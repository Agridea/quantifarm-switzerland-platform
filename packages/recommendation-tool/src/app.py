# region:    -- Imports

import hmac
import json
import logging
import os
import threading
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from pydantic import ValidationError
from rdflib import URIRef

from src.config import Settings, config_app_logger, get_settings
from src.data_sources import (
    Dataset,
    DATSGraphClient,
    FarmerProfileGraphClient,
    TripleStoreClient,
)
from src.filtering import (
    apply_property_filters,
    apply_searchbar_filter,
    create_filter_list,
    update_filter_list,
)
from src.models import (
    FarmerProfileInfo,
    SearchBarFilter,
    SelectedFilters,
    TestCase,
    ValidatedURIRef,
)
from src.models.responses import (
    DATSMainResponse,
    FiltersResponse,
    HTTPError,
    RecommendationListResponse,
    RecommendationWithFiltersResponse,
)
from src.recommendation import (
    RecomAlgoType,
    Recommender,
)

# endregion: -- Imports

# region:    -- App initialisation


standard_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": HTTPError,
        "description": "Cannot find input in the data",
    }
}


def dats_not_found_exception(dats_uri: URIRef) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cannot find DATS URI ({dats_uri}) in DATS graph database."
        "Is the URI correct?",
    )


def load_data(settings: Settings, logger: logging.Logger):
    """Loads all graphs from the triple store into a fresh Dataset."""
    with open(settings.literals_mapping_file_path) as input_file:
        literals_mapping: dict = json.loads(input_file.read())

    dataset = Dataset(
        settings.graphs.dats.uri,
        settings.graphs.dats_translations.uri,
        [tc.uri for tc in settings.graphs.test_cases],
        settings.graphs.testcase_translations.uri,
    )

    triple_store_client = TripleStoreClient(settings.sparql_query_endpoint)
    # Order of loading data here is important,
    # functions depend on previously loaded data
    for uri in dataset.test_case_uris:
        graph_client = dataset.get_test_case_client(uri)
        triple_store_client.load_graph(graph_client)
        graph_client.log_graph_info()

    dats_client = dataset.dats_graph_client()
    triple_store_client.load_graph(dats_client)
    dats_client.load_country_data(settings.country_data_file_path)
    dats_client.load_literals_mapping(literals_mapping)
    dataset.add_literals_mapping(literals_mapping)
    dats_client.log_graph_info()

    translations_client = dataset.dats_translations_graph_client()
    triple_store_client.load_graph(translations_client)
    translations_client.log_graph_info()

    testcase_translations_client = dataset.testcase_translations_graph_client()
    triple_store_client.load_graph(testcase_translations_client)
    testcase_translations_client.log_graph_info()

    filters = create_filter_list(dats_client)
    logger.debug(f"Filters are: {filters}")
    return dataset, filters, literals_mapping


class DataStore:
    """Holds the active data. A reload builds everything first and then swaps the
    references, so requests never see a half-loaded state. Concurrent reload
    requests are coalesced: at most one runs, plus one follow-up if requested
    meanwhile."""

    def __init__(self, settings: Settings, logger: logging.Logger):
        self._settings = settings
        self._logger = logger
        self._guard = threading.Lock()
        self._running = False
        self._pending = False
        self.dataset, self.filters, self.literals_mapping = load_data(settings, logger)

    def reload(self) -> None:
        with self._guard:
            if self._running:
                self._pending = True
                return
            self._running = True
        while True:
            try:
                dataset, filters, mapping = load_data(self._settings, self._logger)
                self.dataset, self.filters, self.literals_mapping = (
                    dataset,
                    filters,
                    mapping,
                )
                self._logger.info("Data refreshed from triple store")
            except Exception:
                self._logger.exception("Refresh failed, keeping previous data")
            with self._guard:
                if self._pending:
                    self._pending = False
                    continue
                self._running = False
                return


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executed at starting the server
    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger("App")
    config_app_logger(app.logger)
    config_app_logger(logging.getLogger("TripleStore"))

    store = DataStore(get_settings(), app.logger)

    app.logger.info("--- Started QuantiFarm Recommendation Tool ---")

    yield {"store": store}

    # Executed at stopping the server
    app.logger.info("--- Stopped QuantiFarm Recommendation Tool ---")


app = FastAPI(
    title="QuantiFarm Recommendation Tool - Version 25.Q1",
    description="The Recommendation Tool is an interactive tool that allows farmers "
    "and advisors to gain insights on the available DATS and request a "
    "recommendation of suitable DATS to their profile.",
    openapi_tags=[
        {
            "name": "Tool",
            "description": "Stable routes for the recommendation tool front-end",
        },
        {
            "name": "Development",
            "description": "Routes for testing (sub-)functionalities of the tool, "
            "possibly unstable.",
        },
    ],
    lifespan=lifespan,
)

# endregion: -- App initialisation

# region:    -- Tool routes


@app.get(
    "/initialize",
    tags=["Tool"],
    description="Provides both the initial recommendation list of all DATS and the "
    "filters with their number of items.",
)
async def init(request: Request) -> RecommendationWithFiltersResponse:
    store = request.state.store
    dats_client = store.dataset.dats_graph_client()
    return RecommendationWithFiltersResponse(
        recommendation_list=dats_client.all_dats,
        filter_list=store.filters,
    )


@app.get(
    "/filters",
    tags=["Tool"],
    description="Provides the list of filters and the number of items affected by "
    "each filter.",
)
async def get_filters(request: Request) -> FiltersResponse:
    return FiltersResponse(filter_list=request.state.store.filters)


@app.get(
    "/dats/all",
    tags=["Tool"],
    description="Provides a recommendation list of all DATS in the database.",
)
async def get_all_dats(request: Request) -> RecommendationListResponse:
    dats_client = request.state.store.dataset.dats_graph_client()
    return RecommendationListResponse(recommendation_list=dats_client.all_dats)


@app.post(
    "/dats/recommend",
    tags=["Tool"],
    description="""Use this Route to Recommend, Filter, and Search through the DATS.""",
)
async def recommend_dats(
    request: Request,
    farmer_profile: FarmerProfileInfo = None,
    selected_filters: SelectedFilters = None,
    searchbar_filter: SearchBarFilter = None,
    algorithm_type: RecomAlgoType = None,
    # Explicit Body() since this is a plain scalar alongside Pydantic-model body
    # params, which FastAPI would otherwise treat as a query parameter.
    language: Annotated[str | None, Body()] = None,
    settings: Settings = Depends(get_settings),
) -> RecommendationWithFiltersResponse:
    app.logger.info("Performing recommendation (production)")

    if farmer_profile is None or farmer_profile.is_empty():
        farmer_profile = FarmerProfileGraphClient.empty()
        algorithm_type = "all_dats"
    else:
        farmer_profile = FarmerProfileGraphClient.from_profile(farmer_profile)

    recommender = (
        Recommender.new([(algorithm_type, "union")])
        if algorithm_type
        else Recommender.new(settings.default_recom_algo_types)
    )

    store = request.state.store
    recommendation_list = recommender.recommend(
        farmer_profile, store.dataset, language=language
    )
    if selected_filters:
        recommendation_list = apply_property_filters(
            recommendation_list, selected_filters
        )
    if searchbar_filter:
        recommendation_list = apply_searchbar_filter(
            recommendation_list, searchbar_filter
        )

    filter_list = update_filter_list(recommendation_list, store.filters)

    return RecommendationWithFiltersResponse(
        recommendation_list=recommendation_list, filter_list=filter_list
    )


@app.get(
    "/dats/main",
    responses={**standard_responses},
    tags=["Tool"],
    description="""Provides general DATS information, and test cases with assessment 
        if relevant, from a DATS URI.<br><br>
        Examples:<br><br>
        - no test cases: `dats_uri`=`https://quantifarm.eu/data/dats/bodemidee`<br><br>
        - with test cases: `dats_uri`=`https://quantifarm.eu/data/dats/kathari_uf1`<br><br>
        - also with test cases: `dats_uri`=`https://quantifarm.eu/data/dats/gaiasense`<br>
          (Some data might be missing in database)<br><br>
        Notes:<br><br>
        - Responds with `testcases: []` if the DATS is not used in a test case.<br><br>
        - Response with `message: "Succes"` if all data could be retrieved, otherwise 
          lists the missing graph data.""",
)
async def get_dats_main_info(
    request: Request,
    dats_uri: ValidatedURIRef | None = None,
    dats_name: str | None = None,
    language: str | None = None,
) -> DATSMainResponse:
    """Provides general DATS information, and test cases with assessment if relevant,
    from a DATS URI."""
    dataset = request.state.store.dataset
    dats_client: DATSGraphClient = dataset.dats_graph_client()
    if dats_uri is None:
        if dats_name is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide either a DATS URI or name."
            )
        else:
            dats_uri = dats_client.get_uri(dats_name)

    if dats_uri is None or not dats_client.contains_dats(dats_uri):
        raise dats_not_found_exception(dats_uri)

    test_case_uris = dats_client.dats_used_in_test_case(dats_uri)
    test_cases: list[TestCase] = list()
    clients_not_found: list[URIRef] = list()
    for uri in test_case_uris:
        if client := dataset.get_test_case_client_by_test_case_uri(uri):
            test_cases.append(client.graph_to_model(language=language))
        else:
            clients_not_found.append(uri)

    try:
        dats_information = dats_client.to_dat_model(dats_uri, language=language)
    except ValidationError as ve:
        raise dats_not_found_exception(dats_uri) from ve

    message = (
        "Succes"
        if not clients_not_found
        else f"No test case graph in database for {', '.join(clients_not_found)}"
    )
    return DATSMainResponse(
        dats_info=dats_information, test_cases=test_cases, message=message
    )


@app.get(
    "/profile_entries/",
    tags=["Tool"],
    description="""Use this Route to obtain all data for creating the 
        farmer profile page for users.""",
)
async def profile_entries(request: Request):
    store = request.state.store
    mapping = store.literals_mapping
    filters = store.filters
    return {
        "farm_type": list(mapping["farm_type"].keys()),
        "farm_type_groups": mapping["farm_type"],

        "language": [option_count.option for option_count in filters.languages],
        "country": [option_count.option for option_count in filters.countries],
        "cost_structures": [option_count.option for option_count in filters.cost_structures],

        "functionalities": list(mapping["functionalities"].keys()),
        "functionality_groups": mapping["functionalities"],

        "benefits": list(mapping["benefits"].keys()),
        "benefit_groups": mapping["benefits"],

        "digital_forms": list(mapping["digital_forms"].keys()),
        "digital_forms_groups": mapping["digital_forms"],
    }


@app.post(
    "/admin/refresh",
    tags=["Tool"],
    status_code=status.HTTP_202_ACCEPTED,
    description="Reloads all data from the triple store in the background. "
    "Requires the X-Refresh-Token header.",
)
async def refresh_data(
    request: Request,
    background_tasks: BackgroundTasks,
    x_refresh_token: Annotated[str | None, Header()] = None,
):
    expected = os.environ.get("REFRESH_TOKEN", "")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Refresh is not configured.",
        )
    if not x_refresh_token or not hmac.compare_digest(x_refresh_token, expected):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    background_tasks.add_task(request.state.store.reload)
    return {"status": "refresh scheduled"}


# endregion: -- Tool routes

# region:    -- Development routes


@app.get("/", description="Initialization", tags=["Development"])
async def root():
    return "App is running, see /docs for OpenAPI docs."


@app.get("/hello_world/", description="Hello World", tags=["Development"])
async def hello_world():
    return "Hello, World! App is online!"


# endregion: -- Development routes
