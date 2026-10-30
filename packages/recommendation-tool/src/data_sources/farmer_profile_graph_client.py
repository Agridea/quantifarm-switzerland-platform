from typing import Self
from uuid import UUID, uuid4

from rdflib import IdentifiedNode, Literal, URIRef
from rdflib.namespace import RDF

from common.qcsm_namespaces import GS1, QCSM, S4AGRI, S4AGRI_NEW
from src.models import FarmerProfileEntry, FarmerProfileInfo

from .graph_client import GraphClient


class FarmerProfileGraphClient(GraphClient):
    @classmethod
    def empty(cls) -> Self:
        id = uuid4()
        client = FarmerProfileGraphClient(
            name=f"FarmerProfile-{id}",
            uri=f"<https://quantifarm.eu/graphs/farmerprofile-{id}>",
            dataset=None,
        )
        client._profile_info = {}
        client._farmer_profile_to_text(client._profile_info)
        client._add_core_knowledge_graph_of_farmer(id)
        return client

    @classmethod
    def from_profile(cls, profile_info: FarmerProfileInfo) -> Self:
        id = uuid4()
        client = FarmerProfileGraphClient(
            name=f"FarmerProfile-{id}",
            uri=f"<https://quantifarm.eu/graphs/farmerprofile-{id}>",
            dataset=None,
        )
        client._profile_info = profile_info
        client._farmer_profile_to_text(profile_info)
        client._add_core_knowledge_graph_of_farmer(id)

        for name, entries in client._profile_info:
            if entries is None:
                continue
            listed = entries if isinstance(entries, list) else [entries]
            for entry in listed:
                client._profile_entry_to_triples(name, entry)
        return client

    def _add_core_knowledge_graph_of_farmer(self, id: UUID) -> None:
        farm = URIRef(f"https://quantifarm.eu/data/Farm-{id}")
        farmer = URIRef(f"https://quantifarm.eu/data/Farmer-{id}")

        self.graph.add((farm, RDF.type, S4AGRI.Farm))
        self.graph.add((farmer, RDF.type, S4AGRI.Farmer))
        self.graph.add((farmer, S4AGRI.managesFarm, farm))
        return

    def _profile_entry_to_triples(
        self, entry_name: str, profile_entry: FarmerProfileEntry
    ):
        match entry_name:
            case "language":
                self.graph.add(
                    (
                        self.farmer_node,
                        S4AGRI_NEW.prefersLanguage,
                        Literal(profile_entry.value),
                    )
                )
            case "farm_type":
                self.graph.add(
                    (
                        self.farm_node,
                        S4AGRI_NEW.hasFarmType,
                        Literal(profile_entry.value),
                    )
                )
            case "country":
                address = URIRef(f"address-{str(self.farm_node)}")
                self.graph.add((self.farm_node, S4AGRI_NEW.hasAddress_FAKE, address))
                self.graph.add((address, RDF.type, GS1.address))
                country = URIRef(
                    f"https://quantifarm.eu/data/countries/{profile_entry.value}"
                )
                self.graph.add((address, GS1.addressCountry, country))
            case "functionalities":
                self.graph.add(
                    (
                        self.farmer_node,
                        QCSM.requiresFunctionality_FAKE,
                        Literal(profile_entry.value),
                    )
                )
            case "benefits":
                self.graph.add(
                    (
                        self.farmer_node,
                        QCSM.wantsBenefits_FAKE,
                        Literal(profile_entry.value),
                    )
                )
            case "digital_forms":
                self.graph.add(
                    (
                        self.farmer_node,
                        QCSM.canUseTechnology_FAKE,
                        Literal(profile_entry.value),
                    )
                )
            # Case for profile entries not used in building KG of farmer profile
            case (
                "environmental_preference"
                | "social_preference"
                | "economic_preference"
                | "other"
            ):
                pass
            case _:
                self._logger.warning(
                    f"Creating triples for FarmerProfileEntry {entry_name} not "
                    f"implemented. Please implement for it to be used in the farmer "
                    f"profile knowledge graph."
                )
        return

    @property
    def farm_type(self) -> str | list[str]:
        if not self._profile_info.farm_type:
            return ""
        return self._profile_info.farm_type.value

    @property
    def language(self) -> str | list[str]:
        if not self._profile_info.language:
            return ""
        return self._profile_info.language.value

    @property
    def country(self) -> str | list[str]:
        if not self._profile_info.country:
            return ""
        return self._profile_info.country.value

    @property
    def digital_forms(self) -> str | list[str]:
        if not self._profile_info.digital_forms:
            return ""
        return self._profile_info.digital_forms.value

    @property
    def benefits(self) -> str | list[str]:
        if not self._profile_info.benefits:
            return ""
        return self._profile_info.benefits.value

    @property
    def functionalities(self) -> str | list[str]:
        if not self._profile_info.functionalities:
            return ""
        return self._profile_info.functionalities.value

    @property
    def description(self) -> str:
        return self._description

    @property
    def farm_node(self) -> IdentifiedNode:
        """Assumes there will only be one farm node in the graph."""
        return self._graph.value(None, RDF.type, S4AGRI.Farm)

    @property
    def farmer_node(self) -> IdentifiedNode:
        """Assumes there will only be one farmer node in the graph."""
        return self._graph.value(None, RDF.type, S4AGRI.Farmer)

    def _farmer_profile_to_text(self, farmer_profile: FarmerProfileInfo | None) -> None:
        def join_entries(
            entries: list[FarmerProfileEntry] | FarmerProfileEntry | None,
        ) -> str:
            if not entries:
                return "none"
            elif isinstance(entries, list):
                return ", ".join([x.value for x in entries])
            else:
                return entries.value

        description = "A farm, "
        if not farmer_profile:
            self._description = description
            return

        if farmer_profile.farm_type:
            description += (
                "With farm type: " + join_entries(farmer_profile.farm_type) + ". \n"
            )
        if farmer_profile.country:
            description += (
                "With country: " + join_entries(farmer_profile.country) + ". \n"
            )
        if farmer_profile.language:
            description += (
                "With language: " + join_entries(farmer_profile.language) + ". \n"
            )
        if farmer_profile.digital_forms:
            description += (
                "With digital form: "
                + join_entries(farmer_profile.digital_forms)
                + ". \n"
            )
        if farmer_profile.functionalities:
            description += (
                "With functionalities form: "
                + join_entries(farmer_profile.functionalities)
                + ". \n"
            )
        if farmer_profile.benefits:
            description += (
                "With benefits form: " + join_entries(farmer_profile.benefits) + ". \n"
            )
        if farmer_profile.other:
            description += "With additional information: " + farmer_profile.other + "."
        self._description = description
