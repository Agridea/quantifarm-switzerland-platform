"""Exports all testcase graphs (testcase0 … testcaseN) and the
testcase-translations graph from a running Fuseki triple store into JSON files.

The resulting JSON files can be re-imported into a different Fuseki instance
(e.g. production) via the companion ``importer`` module, effectively replacing
the testcase data wholesale — useful when subject UUIDs in the target
environment are stale/wrong and need to match the local translations.

Usage:
    # Export from local Fuseki (correct UUIDs)
    python -m testcase_loader.exporter

    # Then import into prod
    TRIPLE_STORE_ENDPOINT=<prod-endpoint> python -m testcase_loader.importer

Environment variables:
    TRIPLE_STORE_ENDPOINT   Base URL of the Fuseki store (default: http://localhost:3030)
    EXPORT_DIR              Output directory for the JSON files (default: ./export)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import requests
from rdflib import Graph, Literal

logger = logging.getLogger(__name__)

TRIPLE_STORE_ENDPOINT = os.getenv("TRIPLE_STORE_ENDPOINT", "http://localhost:3030")
EXPORT_DIR = Path(os.getenv("EXPORT_DIR", "./export"))

TESTCASE_GRAPH_PREFIX = "https://quantifarm.eu/graphs/testcase"
TESTCASE_TRANSLATIONS_GRAPH = "https://quantifarm.eu/graphs/testcase-translations"


def discover_testcase_graphs() -> list[str]:
    """Query Fuseki for all named graphs whose URI starts with the testcase prefix."""
    query = (
        "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } . "
        f"FILTER(STRSTARTS(STR(?g), '{TESTCASE_GRAPH_PREFIX}')) "
        "FILTER(!STRSTARTS(STR(?g), 'https://quantifarm.eu/graphs/testcase-translations')) "
        "} ORDER BY ?g"
    )
    response = requests.get(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/query",
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
    )
    response.raise_for_status()
    results = response.json()["results"]["bindings"]
    graph_uris = [row["g"]["value"] for row in results]
    logger.info(f"Discovered {len(graph_uris)} testcase graph(s)")
    return graph_uris


def read_graph(graph_name: str) -> Graph:
    """Read a named graph from the Fuseki graph store endpoint."""
    logger.info(f"Reading graph {graph_name} ...")
    response = requests.get(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/data",
        params={"graph": graph_name},
        headers={"Accept": "application/n-triples"},
    )
    response.raise_for_status()
    graph = Graph()
    if response.text.strip():
        graph.parse(data=response.text, format="nt")
    logger.info(f"  → {len(graph)} triple(s)")
    return graph


def graph_to_json(graph: Graph) -> list[dict]:
    """Convert an rdflib Graph into a JSON-serializable list of dicts.

    Preserves the RDF node type of the object (URI vs literal) so that
    the importer can reconstruct the graph faithfully.
    """
    from rdflib import URIRef

    entries = []
    for subject, predicate, obj in graph:
        entry: dict = {
            "subject": str(subject),
            "predicate": str(predicate),
            "object": str(obj),
        }
        if isinstance(obj, URIRef):
            entry["type"] = "uri"
        elif isinstance(obj, Literal):
            entry["type"] = "literal"
            if obj.language:
                entry["language"] = obj.language
        entries.append(entry)
    entries.sort(key=lambda e: (e["subject"], e["predicate"], e["object"]))
    return entries


def export_graph(graph_name: str, output_filename: str) -> int:
    """Read a named graph and write it as a JSON file. Returns triple count."""
    graph = read_graph(graph_name)
    entries = graph_to_json(graph)
    output_path = EXPORT_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    logger.info(f"Wrote {len(entries)} entries to {output_path}")
    return len(graph)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Exporting testcase graphs from {TRIPLE_STORE_ENDPOINT}")
    logger.info(f"Output directory: {EXPORT_DIR.resolve()}")

    graph_uris = discover_testcase_graphs()
    total = 0
    for graph_uri in graph_uris:
        # Derive filename from URI: …/testcase12 → testcase12.json
        graph_id = graph_uri.rsplit("/", 1)[-1]
        count = export_graph(graph_uri, f"{graph_id}.json")
        total += count

    trans_count = export_graph(TESTCASE_TRANSLATIONS_GRAPH, "testcase-translations.json")
    total += trans_count

    logger.info(
        f"Export complete. {total} total triples across "
        f"{len(graph_uris)} testcase graph(s) + testcase-translations."
    )