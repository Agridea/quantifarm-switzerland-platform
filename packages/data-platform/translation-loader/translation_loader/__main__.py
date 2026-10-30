"""Pre-translates the free-text fields of DATs into de/fr/it via the DeepL API and
stores the results as language-tagged literals in their own graph
(`https://quantifarm.eu/graphs/dats-translations`), instead of translating on the fly
at request time (see `packages/recommendation-tool/src/translation.py`).

Also pre-translates the small, repeating controlled vocabulary used in testcase
graphs (sustainability/indicator parameter names, product types), storing those in
`https://quantifarm.eu/graphs/testcase-translations`.

Incremental by design: existing translations already present in the translations
graph are never re-requested from DeepL, so re-running this after new DATs were
loaded into `https://quantifarm.eu/graphs/dats` only translates the new/changed
literals.

Environment variables:
    TRIPLE_STORE_ENDPOINT   Base URL of the Fuseki store (default: http://localhost:3030)
    DEEPL_API_KEY           DeepL API key (required unless DRY_RUN is set)
    TARGET_LANGUAGES        Comma-separated target languages (default: "de,fr,it")
    TRANSLATE_ONLY_DAT      Optional: restrict the run to a single DAT, given as
                            either its bare slug (e.g. "gaiasense") or full URI.
                            Intended for trying out the pipeline on one DAT first.
                            When set, the testcase vocabulary job is skipped.
    DRY_RUN                 If "true": only report how many literals would be
                            translated, without calling DeepL or writing anything.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from time import sleep

import requests
from qcsm_namespaces import QCSM
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDFS

# QCSM namespace base URI
QCSM_NS = "https://quantifarm.eu/ontology/"

logger = logging.getLogger(__name__)

TRIPLE_STORE_ENDPOINT = os.getenv("TRIPLE_STORE_ENDPOINT", "http://localhost:3030")
SOURCE_GRAPH_NAME = "https://quantifarm.eu/graphs/dats"
TRANSLATIONS_GRAPH_NAME = "https://quantifarm.eu/graphs/dats-translations"
TESTCASE_TRANSLATIONS_GRAPH_NAME = "https://quantifarm.eu/graphs/testcase-translations"
DATS_NAMESPACE = Namespace("https://quantifarm.eu/data/dats/")

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
TARGET_LANGUAGES = [
    lang.strip().lower()
    for lang in os.getenv("TARGET_LANGUAGES", "de,fr,it").split(",")
    if lang.strip()
]
TRANSLATE_ONLY_DAT = os.getenv("TRANSLATE_ONLY_DAT")
DRY_RUN = os.getenv("DRY_RUN", "false").strip().lower() in ("1", "true", "yes")
TRANSLATIONS_LOAD_FROM_JSON = os.getenv("TRANSLATIONS_LOAD_FROM_JSON", "false").strip().lower() in ("1", "true", "yes")
TRANSLATIONS_JSON_DIR = os.getenv("TRANSLATIONS_JSON_DIR", "/data")

# DeepL expects upper-case target language codes.
# DeepL expects upper-case target language codes. German uses the "DE-CH" (Swiss)
# variant so DeepL uses Swiss orthography (no "ß", always "ss") - the app targets
# Swiss users, and this avoids a known issue where "ß" gets mangled elsewhere
# (e.g. the old Google Translate widget corrupted "ß" into "&").
_DEEPL_TARGET_LANG = {"de": "DE-CH", "fr": "FR", "it": "IT"}

# The DeepL API rejects requests with more than 50 text parameters.
_DEEPL_MAX_TEXTS_PER_REQUEST = 50

# User-facing free-text fields worth translating. Supported languages/countries are
# proper nouns and are intentionally excluded, matching the exclusion already made in
# recommendation-tool/src/translation.py. rdfs:label (the DAT's product/tool name,
# e.g. "gaiasense") is also excluded - it's a proper noun/brand name, not a
# description, and must never be translated.
TRANSLATABLE_PREDICATES = [
    URIRef(f"{QCSM_NS}hasTitle"),
    URIRef(f"{QCSM_NS}hasDescription"),
    RDFS.comment,
    URIRef(f"{QCSM_NS}hasKeyword"),
    URIRef(f"{QCSM_NS}isTargetedTowardsAgriculturalSector"),
    URIRef(f"{QCSM_NS}hasBenefits"),
    URIRef(f"{QCSM_NS}hasCostStructure"),
    URIRef(f"{QCSM_NS}hasDigitalForm"),
    URIRef(f"{QCSM_NS}hasFunctionality"),
]

# Small, repeating controlled vocabulary used across testcase graphs (indicator
# names, product types, impact titles, descriptions) - unlike DAT free text, values 
# repeat a lot across testcases/parcels/years, so the actual number of unique strings 
# is tiny. qcsm:hasSustainabilityParameterName is intentionally excluded: it's only 
# used internally to parse environmental/social/economic scores (see
# recommendation-tool/src/models/test_case.py), never shown as raw text.
TESTCASE_TRANSLATABLE_PREDICATES = [
    URIRef(f"{QCSM_NS}hasIndicatorName"),
    URIRef(f"{QCSM_NS}hasProductType"),
    URIRef(f"{QCSM_NS}hasMainImpactTitle"),
    URIRef(f"{QCSM_NS}hasMainImpactSubtitle"),
    URIRef(f"{QCSM_NS}hasCostRevenueImpactCategory"),
    URIRef(f"{QCSM_NS}hasCostRevenueImpactName"),
    URIRef(f"{QCSM_NS}hasCostRevenueImpactShortDescription"),
    URIRef(f"{QCSM_NS}hasAggregatedImpactName"),
]


def wait_for_connection(ping_url: str, sleep_s: int = 1) -> None:
    connected = False
    while not connected:
        try:
            resp = requests.get(ping_url)
            connected = resp.ok
        except requests.RequestException:
            connected = False
        finally:
            if not connected:
                logger.info("waiting for connection to triple store to be alive...")
                sleep(sleep_s)


def resolve_dat_uri(value: str) -> URIRef:
    """Accept either a full DAT URI or a bare slug (e.g. "gaiasense")."""
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)
    return DATS_NAMESPACE[value]


def load_source_graph(only_dat: URIRef | None) -> Graph:
    """CONSTRUCT the translatable (subject, predicate, literal) triples for all
    DATs (or a single DAT, if `only_dat` is given) from the source `dats` graph.
    """
    predicate_values = ", ".join(p.n3() for p in TRANSLATABLE_PREDICATES)
    dat_filter = f"VALUES ?dat {{ {only_dat.n3()} }}" if only_dat else ""
    query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX qcsm: <https://quantifarm.eu/ontology/>
        CONSTRUCT {{ ?dat ?p ?o }}
        FROM <{SOURCE_GRAPH_NAME}>
        WHERE {{
            ?dat a qcsm:DigitalAgriculturalTechnology .
            {dat_filter}
            ?dat ?p ?o .
            FILTER(?p IN ({predicate_values}))
            FILTER(isLiteral(?o))
        }}
    """
    response = requests.get(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/query",
        params={"query": query},
        headers={"Accept": "application/n-triples"},
    )
    response.raise_for_status()
    graph = Graph()
    if response.text.strip():
        graph.parse(data=response.text, format="nt")
    return graph


def load_testcase_source_graph() -> Graph:
    """CONSTRUCT the translatable (subject, predicate, literal) triples for the
    controlled vocabulary (indicator names, product types) across ALL testcase
    graphs. Uses an explicit `GRAPH ?g` pattern so it works regardless of whether
    the store is configured with a union default graph.
    """
    predicate_values = ", ".join(p.n3() for p in TESTCASE_TRANSLATABLE_PREDICATES)
    query = f"""
        PREFIX qcsm: <https://quantifarm.eu/ontology/>
        CONSTRUCT {{ ?s ?p ?o }}
        WHERE {{
            GRAPH ?g {{
                ?s ?p ?o .
                FILTER(?p IN ({predicate_values}))
                FILTER(isLiteral(?o))
            }}
        }}
    """
    response = requests.get(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/query",
        params={"query": query},
        headers={"Accept": "application/n-triples"},
    )
    response.raise_for_status()
    graph = Graph()
    if response.text.strip():
        graph.parse(data=response.text, format="nt")
    return graph


def get_graph(graph_name: str) -> Graph:
    """Read an existing named graph from the triple store (empty if it doesn't
    exist yet).
    """
    response = requests.get(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/data",
        params={"graph": graph_name},
        headers={"Accept": "application/n-triples"},
    )
    graph = Graph()
    if response.ok and response.text.strip():
        graph.parse(data=response.text, format="nt")
    return graph


def put_graph(graph: Graph, graph_name: str) -> None:
    logger.info(f"PUTting {len(graph)} triples into graph {graph_name}...")
    response = requests.put(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/data",
        params={"graph": graph_name},
        headers={"Content-Type": "application/n-triples"},
        data=graph.serialize(format="nt", encoding="utf-8"),
    )
    response.raise_for_status()


def collect_missing_texts(
    source_graph: Graph, translations_graph: Graph
) -> dict[str, list[tuple[URIRef, URIRef, str]]]:
    """Group (subject, predicate, text) triples that still need a translation,
    keyed by target language. A triple is considered already translated if the
    translations graph already has a language-tagged literal for the same
    subject/predicate/language.
    """
    existing = {
        (subject, predicate, obj.language)
        for subject, predicate, obj in translations_graph
        if isinstance(obj, Literal) and obj.language
    }

    missing: dict[str, list[tuple[URIRef, URIRef, str]]] = {
        lang: [] for lang in TARGET_LANGUAGES
    }
    for subject, predicate, obj in source_graph:
        text = str(obj).strip()
        if not text:
            continue
        for lang in TARGET_LANGUAGES:
            if (subject, predicate, lang) not in existing:
                missing[lang].append((subject, predicate, text))
    return missing


def translate_language(
    entries: list[tuple[URIRef, URIRef, str]],
    lang: str,
    translations_graph: Graph,
) -> int:
    """Translate all missing (subject, predicate, text) triples for a single
    language via DeepL and add the results to `translations_graph`. Returns the
    number of new triples added. Kept per-language (rather than translating every
    language before writing anything) so a checkpoint can be persisted after each
    language - a failure partway through (e.g. quota/network) only risks the
    language currently in progress, not previously completed ones.
    """
    import deepl  # imported lazily so DRY_RUN doesn't require the dependency/key

    if not DEEPL_API_KEY:
        raise RuntimeError(
            "DEEPL_API_KEY is not set - required to actually translate (set "
            "DRY_RUN=true to only see what would be translated, without a key)."
        )
    if not entries:
        return 0

    translator = deepl.Translator(DEEPL_API_KEY)
    # De-dup identical source texts within this language batch to save quota.
    unique_texts = list(dict.fromkeys(text for _, _, text in entries))

    # The DeepL API accepts at most 50 text parameters per request - chunk large
    # batches instead of sending everything in one call (which would otherwise be
    # rejected outright with a "too many text parameters" error).
    translated_by_text: dict[str, str] = {}
    for i in range(0, len(unique_texts), _DEEPL_MAX_TEXTS_PER_REQUEST):
        chunk = unique_texts[i : i + _DEEPL_MAX_TEXTS_PER_REQUEST]
        results = translator.translate_text(chunk, target_lang=_DEEPL_TARGET_LANG[lang])
        translated_by_text.update(zip(chunk, (r.text for r in results)))

    added = 0
    for subject, predicate, text in entries:
        translations_graph.add(
            (subject, predicate, Literal(translated_by_text[text], lang=lang))
        )
        added += 1
    return added


def json_to_graph(json_path: Path) -> Graph:
    """Deserialize a JSON file (produced by the exporter) back into an rdflib
    Graph.  Raises ``FileNotFoundError`` if the file does not exist.
    """
    if not json_path.is_file():
        raise FileNotFoundError(
            f"Translation JSON file not found: {json_path}\n"
            "Run the exporter first (python -m translation_loader.exporter) "
            "or set TRANSLATIONS_JSON_DIR to the correct directory."
        )
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)
    graph = Graph()
    for entry in entries:
        subject = URIRef(entry["subject"])
        predicate = URIRef(entry["predicate"])
        lang = entry.get("language")
        if lang:
            obj = Literal(entry["object"], lang=lang)
        else:
            obj = Literal(entry["object"])
        graph.add((subject, predicate, obj))
    return graph


def load_translations_from_json() -> None:
    """Load pre-exported translation JSON files and PUT them into the triple
    store.  This replaces the normal DeepL-based translation flow and is
    intended for deploying translations to an environment (e.g. production)
    where DeepL should not be called.

    Raises ``FileNotFoundError`` if a required JSON file is missing.
    """
    json_dir = Path(TRANSLATIONS_JSON_DIR)
    jobs = [
        (json_dir / "translations-dats.json", TRANSLATIONS_GRAPH_NAME, "dats"),
        (json_dir / "translations-testcases.json", TESTCASE_TRANSLATIONS_GRAPH_NAME, "testcases"),
    ]
    for json_path, graph_name, label in jobs:
        logger.info(f"[{label}] Loading translations from {json_path} ...")
        graph = json_to_graph(json_path)
        logger.info(f"[{label}] Deserialized {len(graph)} triple(s)")
        put_graph(graph, graph_name)
        logger.info(f"[{label}] PUT complete → {graph_name}")


def run_translation_job(
    source_graph: Graph, translations_graph_name: str, label: str
) -> None:
    """Diff `source_graph` against the existing translations graph, then (unless
    DRY_RUN) translate and persist a checkpoint after each language.
    """
    translations_graph = get_graph(translations_graph_name)
    logger.info(
        f"[{label}] Loaded {len(translations_graph)} existing triple(s) from "
        f"{translations_graph_name}"
    )

    missing = collect_missing_texts(source_graph, translations_graph)
    for lang, entries in missing.items():
        logger.info(f"[{label}] {lang}: {len(entries)} literal(s) still need translation")

    if DRY_RUN:
        logger.info(
            f"[{label}] DRY_RUN is set - not calling DeepL, not writing to the "
            "triple store."
        )
        return

    for lang, entries in missing.items():
        if not entries:
            continue
        added = translate_language(entries, lang, translations_graph)
        logger.info(f"[{label}] Added {added} new {lang} triple(s)")
        put_graph(translations_graph, translations_graph_name)
        logger.info(f"[{label}] Checkpoint saved after {lang}.")
    logger.info(f"[{label}] Done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Connecting to endpoint {TRIPLE_STORE_ENDPOINT}")
    wait_for_connection(f"{TRIPLE_STORE_ENDPOINT}/$/ping")

    if TRANSLATIONS_LOAD_FROM_JSON:
        logger.info("TRANSLATIONS_LOAD_FROM_JSON is set — importing translations from JSON files.")
        load_translations_from_json()
        logger.info("JSON import complete.")
    else:
        only_dat = resolve_dat_uri(TRANSLATE_ONLY_DAT) if TRANSLATE_ONLY_DAT else None
        if only_dat:
            logger.info(f"Restricting this run to a single DAT: {only_dat}")

        source_graph = load_source_graph(only_dat)
        logger.info(
            f"Loaded {len(source_graph)} translatable triple(s) from {SOURCE_GRAPH_NAME}"
        )
        run_translation_job(source_graph, TRANSLATIONS_GRAPH_NAME, label="dats")

        if only_dat is None:
            testcase_source_graph = load_testcase_source_graph()
            logger.info(
                f"Loaded {len(testcase_source_graph)} translatable triple(s) from "
                "testcase graphs"
            )
            run_translation_job(
                testcase_source_graph, TESTCASE_TRANSLATIONS_GRAPH_NAME, label="testcases"
            )
        else:
            logger.info(
                "Skipping testcase vocabulary translation (TRANSLATE_ONLY_DAT is set)."
            )


