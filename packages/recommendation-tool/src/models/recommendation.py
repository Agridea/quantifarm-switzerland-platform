from typing import Annotated, Any, Literal, TypeAlias

from pydantic import BaseModel, BeforeValidator
from rdflib import Literal as RDFLiteral

from .test_case import TestCaseDescription

##########################################
####    FARMER PROFILE MODEL          ####
##########################################


class FarmerProfileEntry(BaseModel):
    value: str
    requireExactMatch: bool


class FarmerProfileInfo(BaseModel):
    farm_type: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    # TODO: name change to plural
    language: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    # TODO: name change to plural
    country: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    functionalities: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    benefits: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    digital_forms: list[FarmerProfileEntry] | FarmerProfileEntry | None = None
    other: str | None = None
    environmental_preference: float | None = None
    social_preference: float | None = None
    economic_preference: float | None = None

    def is_empty(self) -> bool:
        return bool(
            self.farm_type is None
            and self.language is None
            and self.country is None
            and self.functionalities is None
            and self.benefits is None
            and self.digital_forms is None
        )


##########################################
####    DAT MODEL                     ####
##########################################


class BasicDescription(BaseModel):
    ID: str
    name: str
    title: str
    description: str
    keywords: list[str] = []
    test_cases: list[TestCaseDescription]


class FilterableProperties[T](BaseModel):
    agricultural_sectors: T | None = []
    benefits: T | None = []
    cost_structures: T | None = []
    countries: T | None = []
    digital_forms: T | None = []
    functionalities: T | None = []
    languages: T | None = []


def validate_dats_source(input: Any) -> str:
    if isinstance(input, RDFLiteral):
        return input.toPython()
    return input


DATSSources = Annotated[
    Literal["fairshare", "costbenefit", "testcase", "website"],
    BeforeValidator(validate_dats_source),
]


class DATProperties(BaseModel):
    source: list[DATSSources]
    launch_year: str | None = None
    update_year: str | None = None
    web_page: str | None = None


class DATWithExplanation(BaseModel):
    description: BasicDescription
    filterable_properties: FilterableProperties[list[str]]
    properties: DATProperties
    explanation: str | None = None


class DAT(BaseModel):
    description: BasicDescription
    filterable_properties: FilterableProperties[list[str]]
    properties: DATProperties

    def add_explanation(self, explanation: str | None) -> DATWithExplanation:
        return DATWithExplanation(
            description=self.description,
            filterable_properties=self.filterable_properties,
            properties=self.properties,
            explanation=explanation,
        )


##########################################
####    FILTER MODELS                 ####
##########################################


class SearchBarFilter(BaseModel):
    query_string: str
    search_description: bool = True
    search_title: bool = True
    search_keywords: bool = True
    search_functionalities: bool = True
    search_benefits: bool = True


class OptionCount(BaseModel):
    option: str
    count: int


FiltersCount: TypeAlias = FilterableProperties[list[OptionCount]]

SelectedFilters: TypeAlias = FilterableProperties[list[str]]
