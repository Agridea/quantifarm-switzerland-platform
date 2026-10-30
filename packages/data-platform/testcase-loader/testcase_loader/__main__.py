from pathlib import Path
from uuid import uuid4
from qcsm_namespaces import PLOUTOS, WGS84, S4AGRI, SF, GEO, QCSM
import testcase_loader.testcase_data_json_loader as loader
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF
import requests
from time import sleep
import glob
import logging
import os
import sys
import json

logger = logging.getLogger(__name__)

# docker-compose.yml always sets TRIPLE_STORE_ENDPOINT for local use; this is only
# the fallback if the env var isn't set.
TRIPLE_STORE_ENDPOINT = os.environ.get(
    "TRIPLE_STORE_ENDPOINT", "http://triple-store:3030"
)
# Directory to look for TC*.json testcase files in - defaults to the current
# working directory (== /app/testcase-loader in the Docker image).
TESTCASE_DATA_DIR = os.environ.get("TESTCASE_DATA_DIR", ".")
GRAPH_NAME_PREFIX = "https://quantifarm.eu/graphs/testcase"


def wait_for_connection(ping_url, sleep_s=1):
    connected = False
    while not connected:
        try:
            resp = requests.get(ping_url)
            connected = resp.ok
        except:
            pass
        finally:
            if not connected:
                logger.info("waiting for connection to triple store to be alive...")
                sleep(sleep_s)


def put_graph(g: Graph, graph_store_endpoint: str, graph_name: str):
    logger.info("PUTting data into testcase-data graph...")
    requests.put(
        graph_store_endpoint,
        params={"graph": graph_name},
        headers={"Content-Type": "application/n-triples"},
        data=g.serialize(format="nt", encoding="utf-8"),
    )

def get_graph(graph_store_endpoint: str, graph_name: str) -> Graph:
    logger.info("GETting data from testcase-data graph...")
    response = requests.get(
        graph_store_endpoint,
        params={"graph": graph_name},
        headers={"Content-Type": "application/n-triples"}
    )
    if (response.status_code == 200):
        g = response.text
        return g
    else:
        return "null" 

LOAD_FROM_JSON = os.environ.get("TC_LOAD_FROM_JSON", "false").strip().lower() in ("1", "true", "yes")
IMPORT_DIR = os.environ.get("TC_IMPORT_DIR", "./export")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"TRIPLE_STORE_ENDPOINT = {TRIPLE_STORE_ENDPOINT}")
    wait_for_connection(f"{TRIPLE_STORE_ENDPOINT}/$/ping")

    if LOAD_FROM_JSON:
        logger.info("LOAD_FROM_JSON is set — importing testcase graphs from JSON files.")
        from testcase_loader.importer import import_from_directory
        import_from_directory(Path(IMPORT_DIR), TRIPLE_STORE_ENDPOINT)
        logger.info("JSON import complete.")
        sys.exit(0)

    # TESTCASE_FILE (without .json, e.g. "TC1") loads just that one file - useful
    # for testing. By default (not set), all TC*.json files in TESTCASE_DATA_DIR
    # are loaded, one graph per file, non-interactively.
    single_file = os.environ.get("TESTCASE_FILE")
    if single_file:
        json_files = [os.path.join(TESTCASE_DATA_DIR, f"{single_file}.json")]
    else:
        json_files = sorted(glob.glob(os.path.join(TESTCASE_DATA_DIR, "TC*.json")))

    if not json_files:
        logger.info(f"No testcase JSON files found in '{TESTCASE_DATA_DIR}' (looked for TC*.json)")
        sys.exit(1)

    for file in json_files:
        if not os.path.exists(file):
            logger.warning(f"File does not exist, skipping: {file}")
            continue

        logger.info(f"Loading {file}...")
        with open(file, "r") as f:
            data = json.load(f)
        try:
            g, nr = loader.load(data)
        except Exception:
            logger.exception(f"Failed to parse {file}, skipping")
            continue

        graph = f"{GRAPH_NAME_PREFIX}{nr}"
        logger.info(f"Graph name is: {graph} ({len(g)} triples)")
        put_graph(g, f"{TRIPLE_STORE_ENDPOINT}/quantifarm/data", graph)

    logger.info("DONE")
