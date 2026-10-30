import logging

from rdflib import Dataset, Graph, Literal, URIRef

from common.qcsm_namespaces import GS1, QCSM, S4AGRI


class GraphClient:
    initial_namespaces = {
        "gs1": GS1,
        "qcsm": QCSM,
        "s4agri": S4AGRI
    }

    # Languages the translation-loader pre-translates text fields into (see
    # packages/data-platform/translation-loader).
    SUPPORTED_LANGUAGES = {"de", "fr", "it"}
    _translations_graph: Graph | None = None

    def __init__(self, name: str, uri: URIRef, dataset: Dataset | None):
        self._name = name
        self._uri = uri
        if dataset is None:
            self._graph = Graph()
        else:
            self._graph = dataset.graph(uri)
            
        self._logger = logging.getLogger(f"{self._name}-Graph")


    
    def log_graph_info(self) -> None:
        self._logger.info(f"Total number of triples: {len(self._graph)}")
        return

    def set_translations_graph(self, graph: Graph) -> None:
        """Set the graph holding pre-translated (language-tagged) literals, as
        written by the translation-loader. Once set, `_translated_value`/
        `_translated_list` return translated text instead of the original
        (falling back to the original for anything not translated yet).
        """
        self._translations_graph = graph

    def _translated_value(
        self,
        subject: URIRef,
        predicate: URIRef,
        original: Literal | None,
        language: str | None,
    ) -> Literal | None:
        if (
            not language
            or language not in self.SUPPORTED_LANGUAGES
            or self._translations_graph is None
        ):
            return original
        for literal in self._translations_graph.objects(subject, predicate):
            if isinstance(literal, Literal) and literal.language == language:
                return literal
        return original

    def _translated_list(
        self,
        subject: URIRef,
        predicate: URIRef,
        originals: list[Literal],
        language: str | None,
    ) -> list[Literal]:
        if (
            not language
            or language not in self.SUPPORTED_LANGUAGES
            or self._translations_graph is None
        ):
            return originals
        translated = list(
            {
                literal
                for literal in self._translations_graph.objects(subject, predicate)
                if isinstance(literal, Literal) and literal.language == language
            }
        )
        return translated or originals

    @property
    def uri(self) -> URIRef:
        return self._uri
    
    @property
    def graph(self) -> Graph:
        return self._graph