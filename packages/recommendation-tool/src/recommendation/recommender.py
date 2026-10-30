import logging
from typing import Literal, Self

from rdflib import URIRef

from src.data_sources import Dataset, FarmerProfileGraphClient
from src.models import DAT

from .algorithms import (
    RecomAlgo,
    RecomAlgoType,
    ScoredDATS,
    all_dats_recom_algo,
    all_random_dats_recom_algo,
    by_source_recom_algo,
    exact_match_recom_algo,
    metapath_based_recom_algo,
    random_recom_algo,
    sustainability_radix_recom_algo,
    sustainability_scoring_recom_algo,
)

CompositionTypes = Literal["union", "set_a"]


class Recommender:
    """Can execute a series of recommendation algorithms for some
    farmer profile and DATS graph. First algorithm is provided at construction, others
    can be added to the object. Implements a basic Strategy design pattern.

    Args:
        recom_algo_type (RecomAlgoType): Type of recommendation algorithm of
                                        :meth:`recom_algo`, used for logging purposes.
        recom_algo (RecomAlgo): One recommendation algorithm that will be executed in
                                :meth:`Recommender.recommend`. Multiple algorithms can
                                be added using :meth:`Recommender.add_algorithm`.
    """

    def __init__(self) -> None:
        self.algorithms = list()
        self._logger = logging.getLogger("Recommender")
        self._logger.setLevel(logging.INFO)

    @classmethod
    def new(
        cls, recom_algo_types: list[tuple[RecomAlgoType, CompositionTypes]]
    ) -> Self:
        """Builds a :class:`Recommender` object that can execute the recommendation
        algorithms of the given type. First algorithm is provided at construction,
        others can be added to the object. Implements a basic Strategy design pattern.

        Args:
            recom_algo_type (RecomAlgoType): Recommendation algorithm that is executed
                                             in :meth:`Recommender.recommend`
        """
        rec = Recommender()
        for alg, comp in recom_algo_types:
            rec.add_algorithm(alg, comp)
        return rec

    @classmethod
    def _select_algorithm(cls, recom_algo_type: RecomAlgoType) -> RecomAlgo:
        match recom_algo_type:
            case RecomAlgoType.RANDOM:
                return random_recom_algo
            case RecomAlgoType.ALL_RANDOM:
                return all_random_dats_recom_algo
            case RecomAlgoType.ALL_DATS:
                return all_dats_recom_algo
            case RecomAlgoType.EXACT_MATCH:
                return exact_match_recom_algo
            case RecomAlgoType.METAPATH_BASED:
                return metapath_based_recom_algo
            case RecomAlgoType.BY_SOURCE:
                return by_source_recom_algo
            case RecomAlgoType.SUSTAINABILITY_RADIX:
                return sustainability_radix_recom_algo
            case RecomAlgoType.SUSTAINABILITY_SCORING:
                return sustainability_scoring_recom_algo
            case _:
                logging.warning(
                    f"Trying to select algorithm with type "
                    f"{recom_algo_type}, but is not implemented. "
                    f"Defaulting to use of exact-match algorithm."
                )
                return exact_match_recom_algo

    def add_algorithm(
        self, recom_algo_type: RecomAlgoType, composition_type: CompositionTypes
    ) -> None:
        """Add an algorithm of the given type to the recommenders series of algorithms
        executed during recommendation."""
        self.algorithms.append(
            (
                recom_algo_type,
                composition_type,
                Recommender._select_algorithm(recom_algo_type),
            )
        )
        return

    def recommend(
        self,
        farmer_profile: FarmerProfileGraphClient,
        dataset: Dataset,
        language: str | None = None,
    ) -> list[DAT]:
        """Create a recommended list of DATS based on the :class:`Recommender`'s
        recommendation algorithms.
        """
        self._logger.info(
            f"Perform recommendation | Algorithms: {' + '.join(self.algorithm_types)}"
        )

        sorted_dats = self._exec_recommend(farmer_profile, dataset, language=language)

        self._logger.debug(
            "Top results: %s\n...",
            "\n".join(
                [
                    f"DATS: {x[0].description.ID} - score: {x[1]}"
                    for x in sorted_dats[0:10]
                ]
            ),
        )
        return [dats for dats, _ in sorted_dats]

    def recommend_experiment(
        self, farmer_profile: FarmerProfileGraphClient, dataset: Dataset
    ) -> list[tuple[URIRef, float]]:
        """Create a recommended list of DATS based on the :class:`Recommender`'s
        recommendation algorithms.
        """
        sorted_dats = self._exec_recommend(farmer_profile, dataset)
        return [(dats.description.ID, score) for dats, score in sorted_dats]

    def _exec_recommend(
        self,
        farmer_profile: FarmerProfileGraphClient,
        dataset: Dataset,
        language: str | None = None,
    ) -> list[tuple[DAT, float]]:
        """Private inner recommendation function"""

        def build_explanation(
            explanation_a: str | None, explanation_b: str | None
        ) -> str | None:
            explanation = None
            if explanation_a is None:
                explanation = explanation_b
            else:
                explanation = explanation_a
                if explanation_b is not None:
                    explanation += " - " + explanation_b
            return explanation

        # Inner composition of lists function, made to be extended with weights, etc.
        def compose_union(first: ScoredDATS, second: ScoredDATS) -> ScoredDATS:
            for uri, (score_b, explanation_b) in second.items():
                score_a, explanation_a = first.get(uri, (0, None))
                explanation = build_explanation(explanation_a, explanation_b)
                first[uri] = (score_a + score_b, explanation)
            return first

        def compose_set_a(first: ScoredDATS, second: ScoredDATS) -> ScoredDATS:
            for uri, (score_a, explanation_a) in first.items():
                score_b, explanation_b = second.get(uri, (0, None))
                explanation = build_explanation(explanation_a, explanation_b)
                first[uri] = (score_a + score_b, explanation)
            return first

        composed: ScoredDATS = dict()
        for _x, composition_type, algorithm in self.algorithms:
            print(composition_type)
            scored_dats = algorithm(farmer_profile, dataset)
            if composition_type == "union":
                compose_union(composed, scored_dats)
            elif composition_type == "set_a":
                compose_set_a(composed, scored_dats)
            else:
                raise NotImplementedError()

        dats_client = dataset.dats_graph_client()
        composed_tuples = [
            (
                dats_client.to_dat_model(node, language=language).add_explanation(
                    explanation
                ),
                score,
            )
            for node, (score, explanation) in composed.items()
        ]
        composed_tuples.sort(key=lambda x: x[1], reverse=True)
        return composed_tuples

    @property
    def algorithm_types(self) -> list[RecomAlgoType]:
        return [t for t, _, _ in self.algorithms]
