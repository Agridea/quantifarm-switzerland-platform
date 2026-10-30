"""Imports testcase graphs and testcase-translations from JSON files into
a running Fuseki triple store.

Counterpart to ``exporter`` — use together to clone testcase data between
environments (e.g. local → production) while preserving subject UUIDs.

Usage:
    # Import exported graphs into prod
    TRIPLE_STORE_ENDPOINT=<prod-endpoint> python -m testcase_loader.importer

    # Or specify a custom import directory
    IMPORT_DIR=/path/to/export TRIPLE_STORE_ENDPOINT=<prod> python -m testcase_loader.importer

Environment variables:
    TRIPLE_STORE_ENDPOINT   Base URL of the Fuseki store (default: http://localhost:3030)
    IMPORT_DIR              Directory containing the JSON files (default: ./export)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import requests
from rdflib import Graph, Literal, URIRef

logger = logging.getLogger(__name__)

TRIPLE_STORE_ENDPOINT = os.getenv("TRIPLE_STORE_ENDPOINT", "http://localhost:3030")
IMPORT_DIR = Path(os.getenv("IMPORT_DIR", "./export"))

TESTCASE_GRAPH_PREFIX = "https://quantifarm.eu/graphs/testcase"
TESTCASE_TRANSLATIONS_GRAPH = "https://quantifarm.eu/graphs/testcase-translations"


def json_to_graph(json_path: Path) -> Graph:
    """Deserialize a JSON file into an rdflib Graph.

    Each entry is a dict with keys: subject, predicate, object, and
    optionally language (for language-tagged literals) and type ("uri"
    or "literal").  The ``type`` field is used to reconstruct URIRef vs
    Literal nodes faithfully.  Legacy export files without a ``type``
    field fall back to string-prefix heuristics.
    """
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)
    graph = Graph()
    for entry in entries:
        subject = URIRef(entry["subject"])
        predicate = URIRef(entry["predicate"])
        value = entry["object"]
        node_type = entry.get("type")
        lang = entry.get("language")

        if node_type == "uri":
            obj = URIRef(value)
        elif node_type == "literal":
            obj = Literal(value, lang=lang) if lang else Literal(value)
        else:
            # Legacy fallback: treat http(s) URIs as URIRef, rest as Literal
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                obj = URIRef(value)
            else:
                obj = Literal(value, lang=lang) if lang else Literal(value)

        graph.add((subject, predicate, obj))
    return graph


def put_graph(graph: Graph, graph_name: str, endpoint: str | None = None) -> None:
    """PUT a graph into the Fuseki triple store (replaces existing graph)."""
    base = endpoint or TRIPLE_STORE_ENDPOINT
    logger.info(f"PUTting {len(graph)} triples into {graph_name} ...")
    response = requests.put(
        f"{base}/quantifarm/data",
        params={"graph": graph_name},
        headers={"Content-Type": "application/n-triples"},
        data=graph.serialize(format="nt", encoding="utf-8"),
    )
    response.raise_for_status()
    logger.info(f"  → OK ({response.status_code})")


def import_from_directory(import_dir: Path, endpoint: str | None = None) -> None:
    """Import all testcase JSON files from *import_dir* into the Fuseki store at *endpoint*."""
    if not import_dir.exists():
        logger.error(f"Import directory does not exist: {import_dir}")
        raise FileNotFoundError(import_dir)

    testcase_files = sorted(
        p for p in import_dir.glob("testcase*.json")
        if p.name != "testcase-translations.json"
    )
    if not testcase_files:
        logger.warning(f"No testcase JSON files found in {import_dir}")

    total = 0
    for json_path in testcase_files:
        graph_id = json_path.stem
        graph_name = f"{TESTCASE_GRAPH_PREFIX}{graph_id.replace('testcase', '')}"
        graph = json_to_graph(json_path)
        logger.info(f"  {json_path.name}: {len(graph)} triples → {graph_name}")
        put_graph(graph, graph_name, endpoint)
        total += len(graph)

    trans_path = import_dir / "testcase-translations.json"
    if trans_path.exists():
        graph = json_to_graph(trans_path)
        logger.info(f"  {trans_path.name}: {len(graph)} triples → {TESTCASE_TRANSLATIONS_GRAPH}")
        put_graph(graph, TESTCASE_TRANSLATIONS_GRAPH, endpoint)
        total += len(graph)
    else:
        logger.warning(f"Translations file not found, skipping: {trans_path}")

    logger.info(
        f"Import complete. {total} total triples written across "
        f"{len(testcase_files)} testcase graph(s)"
        + (" + testcase-translations." if trans_path.exists() else ".")
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Importing testcase graphs into {TRIPLE_STORE_ENDPOINT}")
    logger.info(f"Input directory: {IMPORT_DIR.resolve()}")

    import_from_directory(IMPORT_DIR)