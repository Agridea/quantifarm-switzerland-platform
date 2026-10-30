from pathlib import Path
from rdflib import Graph

ONTO_FILE = Path(__file__).parent.parent / "qcsm.ttl"


def load_ontology() -> Graph:
    g = Graph()
    g.parse(ONTO_FILE, format="ttl")
    return g


def test_is_an_ontology():
    """
    Test that the ontology can be loaded, contains triples, and defines an ontology.
    """
    g = load_ontology()
    assert len(g) > 0

    res = g.query(
        """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            ASK { ?onto a owl:Ontology }
        """
    )
    assert res
