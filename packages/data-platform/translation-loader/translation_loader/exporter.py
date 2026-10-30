"""Exports the two translation graphs (`dats-translations` and
`testcase-translations`) from a running Fuseki triple store into JSON files.

The resulting JSON files can then be imported into a different Fuseki instance
(e.g. production) via the `TRANSLATIONS_LOAD_FROM_JSON` mode of the translation loader,
bypassing the need to re-translate via DeepL.

Usage:
    python -m translation_loader.exporter

Environment variables:
    TRIPLE_STORE_ENDPOINT   Base URL of the Fuseki store (default: http://localhost:3030)
    EXPORT_DIR              Output directory for the JSON files (default: current directory)
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
EXPORT_DIR = Path(os.getenv("EXPORT_DIR", "."))

# Graph names matching those used by the translation loader
DATS_TRANSLATIONS_GRAPH = "https://quantifarm.eu/graphs/dats-translations"
TESTCASE_TRANSLATIONS_GRAPH = "https://quantifarm.eu/graphs/testcase-translations"

# Output file names (with `translations-` prefix for clarity)
DATS_TRANSLATIONS_FILE = "translations-dats.json"
TESTCASE_TRANSLATIONS_FILE = "translations-testcases.json"


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

    Each dict has the keys: subject, predicate, object, and optionally
    language (for language-tagged literals).
    """
    entries = []
    for subject, predicate, obj in graph:
        entry: dict = {
            "subject": str(subject),
            "predicate": str(predicate),
            "object": str(obj),
        }
        if isinstance(obj, Literal) and obj.language:
            entry["language"] = obj.language
        entries.append(entry)
    # Sort for deterministic output (easier diffs / version control).
    entries.sort(key=lambda e: (e["subject"], e["predicate"], e["object"]))
    return entries


def export_graph(graph_name: str, output_filename: str) -> None:
    """Read a named graph and write it as a JSON file."""
    graph = read_graph(graph_name)
    entries = graph_to_json(graph)
    output_path = EXPORT_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    logger.info(f"Wrote {len(entries)} entries to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Exporting translation graphs from {TRIPLE_STORE_ENDPOINT}")
    logger.info(f"Output directory: {EXPORT_DIR.resolve()}")

    export_graph(DATS_TRANSLATIONS_GRAPH, DATS_TRANSLATIONS_FILE)
    export_graph(TESTCASE_TRANSLATIONS_GRAPH, TESTCASE_TRANSLATIONS_FILE)

    logger.info("Export complete.")
