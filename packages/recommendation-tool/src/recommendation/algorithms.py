import json
import random
from collections.abc import Callable
from statistics import mean

from rdflib import Literal, URIRef
from strenum import StrEnum

import src.recommendation.metapath as mp
import src.recommendation.querybuilder as qb
from common.qcsm_namespaces import QCSM
from src.data_sources import Dataset, FarmerProfileGraphClient
from src.models import FarmerProfileInfo

type ScoredDATS = dict[URIRef, tuple[float, str]]
# Recommendation algorithm interface
RecomAlgo = Callable[[FarmerProfileGraphClient, Dataset], ScoredDATS]


class RecomAlgoType(StrEnum):
    EXACT_MATCH = "exact"
    METAPATH_BASED = "metapath"
    ALL_DATS = "all"
    RANDOM = "random"
    ALL_RANDOM = "all random"
    BY_SOURCE = "source"
    SUSTAINABILITY_RADIX = "radix"
    SUSTAINABILITY_SCORING = "scoring"


def profile_required_for_recom_algo(algo_type: RecomAlgoType) -> bool:
    match algo_type:
        case RecomAlgoType.EXACT_MATCH:
            return True
        case RecomAlgoType.METAPATH_BASED:
            return True
        case RecomAlgoType.ALL_DATS:
            return False
        case RecomAlgoType.RANDOM:
            return False
        case RecomAlgoType.ALL_RANDOM:
            return False
        case RecomAlgoType.BY_SOURCE:
            return False
        case RecomAlgoType.SUSTAINABILITY_RADIX:
            return True
        case RecomAlgoType.SUSTAINABILITY_SCORING:
            return True
        case None:
            return False
        # Case for missing implementation, require farmer profile just in case
        case _:
            return True


def random_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    dats_client = dataset.dats_graph_client()
    choice_index = random.randint(0, len(dats_client.all_dats_nodes) - 1)
    return {dats_client.all_dats_nodes[choice_index]: (1.0, None)}


def all_random_dats_recom_algo(
    farmer_profile: FarmerProfileGraphClient | None, dataset: Dataset
) -> ScoredDATS:
    dats_client = dataset.dats_graph_client()
    dats = {
        dat: (round(random.uniform(0, 1), 2), None)
        for dat in dats_client.all_dats_nodes
    }
    return dats


def all_dats_recom_algo(
    farmer_profile: FarmerProfileGraphClient | None, dataset: Dataset
) -> ScoredDATS:
    dats_client = dataset.dats_graph_client()
    return {dat: (0.0, None) for dat in dats_client.all_dats_nodes}


def exact_match_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    dats_client = dataset.dats_graph_client()
    query = qb.build_recommend_query(
        farmer_profile._profile_info,
        farmer_profile._logger,
        dataset.literals_mapping,
        # dats_client.literals_mapping,
    )
    result = dats_client.graph.query(query)
    return {node.dat: (1.0, None) for node in result}


def metapath_based_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    with open("config/meta-paths.json") as mp_file:
        raw_meta_paths = json.loads(mp_file.read())
    metapaths = [
        mp.MetaPath.model_validate(path) for path in raw_meta_paths["metapaths"]
    ]

    start_node = farmer_profile.farmer_node
    dataset.add_graph(farmer_profile)

    # Similarity measure calculation per meta-path
    similarity_scores = dict()
    for path in metapaths:
        similarity_scores[path.ID] = mp.nodes_with_similarity(
            start_node, path, dataset.multigraph
        )

    dataset.remove_graph(farmer_profile)

    # Composition of similarity scores per end node
    recommendation_with_scores = mp.score_composition(similarity_scores, metapaths)
    return recommendation_with_scores


def by_source_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    scored_dats = dict()
    dats_client = dataset.dats_graph_client()
    scored_dats.update(
        {
            dats: (100.0, None)
            for dats in dats_client.graph.subjects(
                QCSM.hasSource, Literal("costbenefit")
            )
        }
    )
    scored_dats.update(
        {
            dats: (200.0, None)
            for dats in dats_client.graph.subjects(QCSM.hasSource, Literal("testcase"))
        }
    )
    return scored_dats


SUSTAINABILITY_RECOMMENDATION_FACTOR = 2.0


def list_dats_sustainability_params(dataset: Dataset) -> list:
    listed_dats = []
    dats_client = dataset.dats_graph_client()

    for dats in dats_client.all_dats_nodes:
        environmental = []
        social = []
        economic = []
        if not (test_cases_uris := dats_client.dats_used_in_test_case(dats)):
            continue

        for tc_uri in test_cases_uris:
            test_case = dataset.get_test_case_client_by_test_case_uri(
                tc_uri
            ).graph_to_model()

            environmental.extend(
                [
                    a.sustainability.environmental
                    for a in test_case.assessments
                    if a.sustainability.environmental is not None
                ]
            )
            social.extend(
                [
                    a.sustainability.social
                    for a in test_case.assessments
                    if a.sustainability.social is not None
                ]
            )
            economic.extend(
                [
                    a.sustainability.economic
                    for a in test_case.assessments
                    if a.sustainability.economic is not None
                ]
            )

        listed_dats.append(
            (
                dats,
                mean(environmental) if environmental else 0,
                mean(social) if social else 0,
                mean(economic) if economic else 0,
            )
        )
    return listed_dats


def sustainability_radix_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    fp: FarmerProfileInfo = farmer_profile._profile_info
    if (
        fp == {}
        or fp.economic_preference is None
        or fp.social_preference is None
        or fp.environmental_preference is None
    ):
        return {}

    def radix_sorting_order():
        prefs = [
            (fp.environmental_preference, 1),
            (fp.social_preference, 2),
            (fp.economic_preference, 3),
        ]
        prefs.sort(key=lambda x: x[0], reverse=True)
        return lambda d: (d[prefs[0][1]], d[prefs[1][1]], d[prefs[2][1]])

    def create_explanation(index: int) -> str | None:
        if index <= 2:
            return "Matches your sustainability preferences well"
        return None

    listed_dats = list_dats_sustainability_params(dataset)
    listed_dats.sort(key=radix_sorting_order(), reverse=True)

    scored_dats = {
        dats: (SUSTAINABILITY_RECOMMENDATION_FACTOR / (i + 1), create_explanation(i))
        for i, (dats, _, _, _) in enumerate(listed_dats)
    }
    return scored_dats


def sustainability_scoring_recom_algo(
    farmer_profile: FarmerProfileGraphClient, dataset: Dataset
) -> ScoredDATS:
    fp: FarmerProfileInfo = farmer_profile._profile_info
    if (
        fp == {}
        or fp.economic_preference is None
        or fp.social_preference is None
        or fp.environmental_preference is None
    ):
        return {}

    def create_explanation(index: int, score: float) -> str | None:
        text = ""
        if score > 0:
            text += "Matches your sustainability preferences"
            if index <= 2:
                text += " well"
            return text
        return None

    listed_dats = list_dats_sustainability_params(dataset)
    listed_dats = [
        (
            dats,
            env * fp.environmental_preference
            + soc * fp.social_preference
            + eco * fp.economic_preference,
        )
        for (dats, env, soc, eco) in listed_dats
    ]
    listed_dats.sort(key=lambda x: x[1], reverse=True)
    max_score = max([score for _, score in listed_dats])
    scored_dats = {
        dats: (
            s := SUSTAINABILITY_RECOMMENDATION_FACTOR * score / max_score
            if max_score > 0
            else 0,
            create_explanation(i, s),
        )
        for i, (dats, score) in enumerate(listed_dats)
    }

    return scored_dats
