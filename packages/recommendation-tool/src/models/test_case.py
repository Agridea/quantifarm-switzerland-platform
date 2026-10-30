from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, Field, field_validator, model_serializer

from .rdf import ValidatedURIRef

DifferenceTypes = Literal["absolute", "percentage", "combined", "None"]


class TestCaseParameterDifference(BaseModel):
    type: DifferenceTypes
    unit: str | None = None
    absolute: float | None = None
    percentage: float | None = None
    value: float | None = None

    def serialize(self) -> dict:
        match self.type:
            case "None":
                return None
            case "absolute":
                return self.model_dump(exclude=["absolute", "percentage"])
            case "percentage":
                return self.model_dump(exclude=["absolute", "percentage", "unit"])
            case "combined":
                return self.model_dump(exclude=["value"])


class TestCaseParameter(BaseModel):
    name: str
    difference: TestCaseParameterDifference | None

    @model_serializer(mode="plain")
    def serialize(self) -> dict:
        return {"name": self.name, "difference": self.difference.serialize()}


class SustainabilityParameters(BaseModel):
    environmental: float | None = Field(
        ...,
        validation_alias=AliasChoices("envionmental sustainability", "environmental"),
    )
    social: float | None = Field(
        ..., validation_alias=AliasChoices("social sustainability", "social")
    )
    economic: float | None = Field(
        ..., validation_alias=AliasChoices("economic sustainability", "economic")
    )

    @field_validator("environmental", "social", "economic", mode='plain')
    @classmethod
    def validate_param(cls, input: Any) -> float | None:
        if input == 'None':
            return None
        return float(input)


class TestCaseAssessmentInfo(BaseModel):
    year: int
    parcel: ValidatedURIRef
    product: str
    sustainability: SustainabilityParameters
    indicators: list[TestCaseParameter]


class TestCaseDATS(BaseModel):
    uri: ValidatedURIRef
    name: str


class TestCaseDescription(BaseModel):
    uri: ValidatedURIRef
    number: int


class TestCase(BaseModel):
    description: TestCaseDescription
    dats: list[TestCaseDATS]
    assessments: list[TestCaseAssessmentInfo]
