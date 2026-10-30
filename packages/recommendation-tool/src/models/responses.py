from pydantic import BaseModel

from .recommendation import DAT, DATWithExplanation, FiltersCount
from .test_case import TestCase


class HTTPError(BaseModel):
    detail: str


class DATSMainResponse(BaseModel):
    dats_info: DAT
    test_cases: list[TestCase]
    message: str


class RecommendationListResponse(BaseModel):
    recommendation_list: list[DATWithExplanation]
    
class FiltersResponse(BaseModel):
    filter_list: FiltersCount

class RecommendationWithFiltersResponse(BaseModel):
    recommendation_list: list[DATWithExplanation]
    filter_list: FiltersCount
    