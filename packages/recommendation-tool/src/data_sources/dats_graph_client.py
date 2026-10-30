import json

from rdflib import IdentifiedNode, Literal, URIRef
from rdflib.namespace import RDF, RDFS

from common.qcsm_namespaces import GS1, QCSM
from src.models import (
    DAT,
    BasicDescription,
    DATProperties,
    FilterableProperties,
    TestCaseDescription,
)

from .graph_client import GraphClient


class DATSGraphClient(GraphClient):
    literals_mapping = None

    def load_country_data(self, file_path: str) -> None:
        self._logger.info(f"Loading country data into graph from file {file_path}...")
        with open(file_path) as input_file:
            input = json.loads(input_file.read())
        for entry in input:
            e = entry["Name"].replace(" ", "_")
            country = URIRef(f"https://quantifarm.eu/data/countries/{e}")
            self._graph.add((country, RDF.type, GS1.Country))
            self._graph.add((country, RDFS.label, Literal(entry["Name"])))
            self._graph.add((country, GS1.countryCode, Literal(entry["Code"])))
        self._logger.info(
            f"The graph contains {
                len([n for n in self._graph.subjects(RDF.type, GS1.Country, True)])
            } country nodes"
        )
        return

    def load_literals_mapping(self, literals_mapping: dict) -> None:
        for _property, options in literals_mapping.items():
            for option_name, mapping in options.items():
                for x in mapping:
                    self._graph.add(
                        (Literal(option_name), QCSM.mapsTo_FAKE, Literal(x))
                    )
        self.literals_mapping = literals_mapping
        return

    def contains_dats(self, dats_node: URIRef) -> bool:
        """Return if the provided DATS URI exists in the graph or not."""
        return (dats_node, RDF.type, QCSM.DigitalAgriculturalTechnology) in self._graph

    def dats_used_in_test_case(self, dats_node: URIRef) -> list[URIRef]:
        """If the provided DATS is used in (a) test case(s),
        return the test case URI(s).

        Args:
            dats_node (URIRef): URI of the DATS of interest.

        Returns:
            The URI(s) of the test case(s) if the DATS is used in any, otherwise
            an empty list.
        """
        return list(self._graph.objects(dats_node, QCSM.isUsedInTestcase, True))

    def get_country_node_by_name(self, name: str) -> IdentifiedNode:
        for node in self._graph.subjects(RDF.type, GS1.Country):
            if self._graph.value(
                node, RDFS.label, Literal(name)
            ):  # TODO: value takes at least one None?
                return node

    def get_number_from_test_case_uri(self, uri: URIRef) -> int:
        return int(uri.removeprefix("https://quantifarm.eu/data/testcases/testcase"))

    def _translated_value(
        self, dat_node: URIRef, predicate: URIRef, language: str | None
    ) -> Literal | None:
        """Return the pre-translated literal for `predicate` in `language` from the
        translations graph, falling back to the original-language value from the
        main graph if no translation is available (yet).
        """
        return super()._translated_value(
            dat_node, predicate, self._graph.value(dat_node, predicate), language
        )

    def _translated_list(
        self, dat_node: URIRef, predicate: URIRef, language: str | None
    ) -> list[Literal]:
        """Same as `_translated_value`, but for predicates with multiple values
        (e.g. keywords). Falls back to the original values if none of them have
        been translated (yet) into `language`.
        """
        return super()._translated_list(
            dat_node,
            predicate,
            self._objects_from_predicate(dat_node, predicate),
            language,
        )

    def to_dat_model(self, dat_node: URIRef, language: str | None = None) -> DAT:
        """Build a `DAT` model from the graph. If `language` is one of
        `SUPPORTED_LANGUAGES`, free-text fields are taken from the translations
        graph (see `set_translations_graph`) instead of their original language,
        falling back to the original text for anything not translated yet.
        Countries/supported languages are proper nouns and are never translated.
        Neither is `name` (rdfs:label) - it's the DAT's product/brand name.
        """
        return DAT(
            description=BasicDescription(
                ID=dat_node,
                name=self._graph.value(dat_node, RDFS.label),
                title=self._translated_value(dat_node, QCSM.hasTitle, language),
                description=self._translated_value(dat_node, RDFS.comment, language),
                keywords=self._translated_list(dat_node, QCSM.hasKeyword, language),
                test_cases=[
                    TestCaseDescription(
                        uri=x, number=self.get_number_from_test_case_uri(x)
                    )
                    for x in self._objects_from_predicate(
                        dat_node, QCSM.isUsedInTestcase
                    )
                ],
            ),
            filterable_properties=FilterableProperties[list[str]](
                agricultural_sectors=self._translated_list(
                    dat_node, QCSM.isTargetedTowardsAgriculturalSector, language
                ),
                countries=[
                    self._graph.value(node, RDFS.label, None)
                    for node in self._objects_from_predicate(
                        dat_node, QCSM.isTargetedTowardsCountry
                    )
                ],
                languages=self._objects_from_predicate(
                    dat_node, QCSM.hasSupportedLanguage
                ),
                cost_structures=self._translated_list(
                    dat_node, QCSM.hasCostStructure, language
                ),
                benefits=self._translated_list(dat_node, QCSM.hasBenefits, language),
                digital_forms=self._translated_list(
                    dat_node, QCSM.hasDigitalForm, language
                ),
                functionalities=self._translated_list(
                    dat_node, QCSM.hasFunctionality, language
                ),
            ),
            properties=DATProperties(
                source=self._objects_from_predicate(dat_node, QCSM.hasSource),
                launch_year=self._graph.value(dat_node, QCSM.hasLaunchYear),
                update_year=self._graph.value(dat_node, QCSM.lastUpdateYear),
                web_page=self._graph.value(dat_node, QCSM.hasWebPage),
            ),
        )

    def _objects_from_predicate(
        self, dat_node: URIRef, predicate: URIRef
    ) -> list[Literal]:
        return list(
            self._graph.objects(subject=dat_node, predicate=predicate, unique=True)
        )
    
    def get_uri(self, dats_name: str) -> URIRef | None:
        name = self._graph.value(None, RDFS.label, Literal(dats_name), default=None)
        return name
        

    @property
    def all_dats_nodes(self) -> list[URIRef]:
        return [
            dat_node
            for dat_node in self._graph.subjects(
                RDF.type, QCSM.DigitalAgriculturalTechnology, True
            )
        ]

    @property
    def all_dats(self) -> list[DAT]:
        return [
            self.to_dat_model(dat_node).add_explanation("Listed all DATS")
            for dat_node in self._graph.subjects(
                RDF.type, QCSM.DigitalAgriculturalTechnology, True
            )
        ]
