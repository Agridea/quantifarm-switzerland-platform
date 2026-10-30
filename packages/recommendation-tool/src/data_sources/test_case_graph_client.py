from functools import cached_property
from itertools import groupby, tee
from typing import Any

from rdflib import RDF, URIRef
from rdflib.plugins.sparql import prepareQuery

from common.qcsm_namespaces import QCSM
from src.models import (
    SustainabilityParameters,
    TestCase,
    TestCaseDescription,
    TestCaseParameter,
    TestCaseParameterDifference,
)

from .graph_client import GraphClient


class TestCaseGraphClient(GraphClient):
    # SPARQL QUERIES
    select_dats_query = prepareQuery(
        queryString=(
            """
            SELECT ?name
            WHERE {{ 
                ?uri rdf:type qcsm:Testcase . 
                ?uri qcsm:hasDatsInformation ?dats . 
                ?dats rdf:type qcsm:DatsInformation . 
                ?dats qcsm:hasDatsName ?name .
            }}
            """
        ),
        initNs=GraphClient.initial_namespaces,
    )

    # Sustainability and indicator info queries are near copies, differing in two
    # predicates. Not ideal, but workable currently.
    select_sustainability_assessment_info_query = prepareQuery(
        queryString=(
            """
            SELECT ?year ?info ?assessment ?parcel ?product ?paramName ?absDifference 
                   ?unit ?percDifference
            WHERE {{ 
                ?uri rdf:type qcsm:Testcase .
                ?uri qcsm:hasYearlyAssessmentInformation ?info . 
                ?info qcsm:hasCultivationYear ?year . 
                ?info qcsm:hasParcelComparison ?comparison .
                ?comparison qcsm:hasParcelAssessmentWithDATS ?assessment .
                ?assessment qcsm:hasParcelInformation ?parcel .
                ?parcel qcsm:hasProductType ?product .
                ?comparison qcsm:hasCalculatedSustainabilityInformation ?sustainInfo . 
                ?sustainInfo qcsm:hasSustainabilityParameterName ?paramName .
                ?sustainInfo qcsm:hasAbsoluteDifference ?absDifference .
                ?sustainInfo qcsm:hasSustainabilityParameterUnit ?unit . 
                ?sustainInfo qcsm:hasPercentageDifference ?percDifference .
            }}
            """
        ),
        initNs=GraphClient.initial_namespaces,
    )

    select_indicator_info_query = prepareQuery(
        queryString=(
            """
            SELECT ?year ?info ?assessment ?parcel ?product ?indicatorInfo ?paramName
                   ?absDifference ?unit ?percDifference
            WHERE {{
                ?uri rdf:type qcsm:Testcase .
                ?uri qcsm:hasYearlyAssessmentInformation ?info .
                ?info qcsm:hasCultivationYear ?year .
                ?info qcsm:hasParcelComparison ?comparison .
                ?comparison qcsm:hasParcelAssessmentWithDATS ?assessment .
                ?assessment qcsm:hasParcelInformation ?parcel .
                ?parcel qcsm:hasProductType ?product .
                ?comparison qcsm:hasCalculatedIndicatorInformation ?indicatorInfo .
                ?indicatorInfo qcsm:hasIndicatorName ?paramName .
                ?indicatorInfo qcsm:hasAbsoluteDifference ?absDifference .
                ?indicatorInfo qcsm:hasIndicatorUnit ?unit .
                ?indicatorInfo qcsm:hasPercentageDifference ?percDifference .
            }}
            """
        ),
        initNs=GraphClient.initial_namespaces,
    )

    # METHODS
    def graph_to_model(self, language: str | None = None) -> TestCase:
        # Select DATS in test case
        query_result = self._graph.query(self.select_dats_query)
        dats = [{"uri": "TODO", "name": row.name} for row in query_result]
        # Select yearly assessment information in test case
        sustainability_query_result = self._graph.query(
            self.select_sustainability_assessment_info_query
        )
        grouped_sustainability_info = self._group_sustainability_params(
            sustainability_query_result
        )
        indicator_query_result = self._graph.query(self.select_indicator_info_query)
        grouped_indicator_info = self._group_graph_params(
            indicator_query_result, language
        )
        # Construct assessment info
        assessments = [
            {
                "year": year,
                "parcel": parcel,
                "product": self._translated_value(
                    parcel, QCSM.hasProductType, product, language
                ),
                "sustainability": info,
                "indicators": grouped_indicator_info[(year, parcel, product)],
            }
            for (year, parcel, product), info in grouped_sustainability_info.items()
        ]
        return TestCase(
            description=TestCaseDescription(uri=self.test_case, number=self.number),
            dats=dats,
            assessments=assessments,
        )

    def _group_sustainability_params(self, query_result: Any) -> dict:
        """To be used specifically with query results from this class's assessment
        info queries. Groups by year, parcel and product on the parcel.
        """
        result = dict()
        for (year, _, parcel, product), params in groupby(
            query_result,
            lambda row: (
                row.year,
                row.assessment,
                row.parcel,
                row.product,
            ),
        ):
            as_dict = {
                param.paramName.toPython(): param.percDifference.toPython()
                for param in params
            }
            result[(year.toPython(), parcel, product.toPython())] = (
                SustainabilityParameters.model_validate(as_dict)
            )
        return result

    def _group_graph_params(self, query_result: Any, language: str | None = None) -> dict:
        """To be used specifically with query results from this class's assessment
        info queries. Groups by year, parcel and product on the parcel.
        """
        return {
            (year.toPython(), parcel, product.toPython()): [
                self._parameter_subgraph_to_model(param, language) for param in params
            ]
            for (year, _, parcel, product), params in groupby(
                query_result,
                lambda row: (row.year, row.assessment, row.parcel, row.product),
            )
        }

    def _parameter_subgraph_to_model(
        self, subgraph: Any, language: str | None = None
    ) -> TestCaseParameter:
        """To be used specifically with query results per parameters from this
        class's assessment info queries.
        """
        name = self._translated_value(
            subgraph.indicatorInfo, QCSM.hasIndicatorName, subgraph.paramName, language
        )
        match (
            absolute := subgraph.absDifference.toPython(),
            percentage := subgraph.percDifference.toPython(),
        ):
            case ("None", "None"):
                difference = TestCaseParameterDifference(type="None")
            case (_, "None"):
                difference = TestCaseParameterDifference(
                    type="absolute",
                    unit=subgraph.unit,
                    absolute=absolute,
                    value=absolute,
                )
            case ("None", _):
                difference = TestCaseParameterDifference(
                    type="percentage", percentage=percentage, value=percentage
                )
            case (_, _):
                difference = TestCaseParameterDifference(
                    type="combined",
                    unit=subgraph.unit,
                    absolute=absolute,
                    percentage=percentage,
                )
        return TestCaseParameter(name=name, difference=difference)

    @cached_property
    def test_case(self) -> URIRef:
        return self._graph.value(None, RDF.type, QCSM.Testcase)

    @cached_property
    def number(self) -> int:
        return int(self._graph.value(self.test_case, QCSM.hasTestcaseNumber, None))
