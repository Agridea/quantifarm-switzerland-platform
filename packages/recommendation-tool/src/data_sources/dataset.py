from rdflib import RDF, URIRef
from rdflib import Dataset as RDFDataset

from common.qcsm_namespaces import QCSM

from .dats_graph_client import DATSGraphClient
from .graph_client import GraphClient
from .test_case_graph_client import TestCaseGraphClient


class Dataset:
    literals_mapping = None

    def __init__(
        self,
        dats_graph_uri: URIRef,
        dats_translations_graph_uri: URIRef,
        test_case_graph_uris: list[URIRef],
        testcase_translations_graph_uri: URIRef,
    ):
        self._multigraph = RDFDataset()
        self._test_case_uris = test_case_graph_uris
        self._dats_graph = self._multigraph.graph(dats_graph_uri)
        self._dats_translations_graph_uri = URIRef(dats_translations_graph_uri)
        self._multigraph.graph(self._dats_translations_graph_uri)
        self._testcase_translations_graph_uri = URIRef(testcase_translations_graph_uri)
        self._multigraph.graph(self._testcase_translations_graph_uri)
        for graph_uri in test_case_graph_uris:
            self._multigraph.graph(URIRef(graph_uri))
        return

    def add_literals_mapping(self, literals_mapping: dict) -> None:
        self.literals_mapping = literals_mapping

    def add_graph(self, client: GraphClient) -> None:
        g = self._multigraph.graph(client.graph.identifier)
        g += client.graph
        return

    def remove_graph(self, client: GraphClient) -> None:
        _ = self._multigraph.remove_graph(client.graph)
        return

    def dats_graph_client(self) -> DATSGraphClient:
        client = DATSGraphClient(
            name="DATS",
            uri=URIRef("https://quantifarm.eu/graphs/dats"),
            dataset=self.multigraph,
        )
        client.set_translations_graph(
            self._multigraph.graph(self._dats_translations_graph_uri)
        )
        return client

    def dats_translations_graph_client(self) -> GraphClient:
        return GraphClient(
            name="DATSTranslations",
            uri=self._dats_translations_graph_uri,
            dataset=self.multigraph,
        )

    def testcase_translations_graph_client(self) -> GraphClient:
        return GraphClient(
            name="TestcaseTranslations",
            uri=self._testcase_translations_graph_uri,
            dataset=self.multigraph,
        )

    def get_test_case_client(self, graph_uri: URIRef) -> TestCaseGraphClient | None:
        graphs = [g.identifier for g in self._multigraph.graphs()]
        if graph_uri not in graphs:
            return None
        client = TestCaseGraphClient(name="temp", uri=graph_uri, dataset=self.multigraph)
        client.set_translations_graph(
            self._multigraph.graph(self._testcase_translations_graph_uri)
        )
        return client

    def get_test_case_client_by_test_case_uri(
        self, test_case_uri: URIRef
    ) -> TestCaseGraphClient | None:
        g = list(
            filter(
                lambda g: g.value(None, RDF.type, QCSM.Testcase) == test_case_uri,
                self._multigraph.graphs(),
            )
        )
        if g == []:
            return None
        else:
            client = TestCaseGraphClient(
                name="temp", uri=g[0].identifier, dataset=self.multigraph
            )
            client.set_translations_graph(
                self._multigraph.graph(self._testcase_translations_graph_uri)
            )
            return client

    @property
    def test_case_uris(self) -> list[URIRef]:
        return self._test_case_uris

    @property
    def multigraph(self) -> RDFDataset:
        return self._multigraph
