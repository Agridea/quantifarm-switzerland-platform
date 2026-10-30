import logging
from collections import defaultdict
from typing import Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator
from rdflib import RDF, Literal, URIRef
from rdflib import Dataset as RDFDataset

from common.qcsm_namespaces import QCSM
from src.models import ValidatedURIRef


class MetaPath(BaseModel):
    """Meta path as defined by Sun et al. in "PathSim: Meta Path-Based Top-K Similarity
    Search in Heterogeneous Information Networks", applied to knowledge graphs.

    Domains and ranges of relations are not compared to the given node types, so the
    user is trusted to set op the meta-paths correctly. Could be extended later to
    include a domain and range test for constructing meta-paths.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    ID: UUID = Field(default_factory=lambda: uuid4(), exclude=True)
    start_node_type: ValidatedURIRef
    node_types: list[ValidatedURIRef]
    relations: list[ValidatedURIRef]
    reverse_relations: list[bool]
    weight: float
    explanation_text: str
    title: str

    @property
    def length(self) -> int:
        return len(self.relations)

    @model_validator(mode="after")
    def check_list_lengths(self) -> Self:
        if len(self.node_types) != len(self.relations) or len(self.node_types) != len(
            self.reverse_relations
        ):
            raise ValueError(
                f"Metapath {''} validation not succesful, length of lists of node types"
                f" ({len(self.node_types)}), relations ({len(self.relations)}) and "
                f"reverse relations ({len(self.reverse_relations)}) not equal."
            )
        return self


def count_instances_by_end_node(
    metapath: MetaPath, start_node: URIRef | Literal, multigraph: RDFDataset
) -> tuple[dict[URIRef | Literal, int], int]:
    """Given some graph, find the end node of all meta-path instances starting in some 
    start node, and count the number of instances ending in each end node. Results are 
    produced using a depth-first search-style algorithm. It also returns the number of 
    branches initiated (leading to a completed path instance or not) in the algorithm, 
    which can be used for a similarity measure implementation.

    Args:
        graph (Graph): Graph in which to find meta-path instances.
        start_node (URIRef | Literal): The node (literals also allowed) in the graph 
                                       where all instances must start.
        metapath (MetaPath): The meta-path of which to find instances.

    Returns:
        Dictionary of end nodes of path instances and the number of instances ending 
        there. \\ Also returns the number of branches initiated in the DFS algorithm. \\
        Returns empty dictionary and zero when error occurs.
    """
    logger = logging.getLogger("Recommender")

    def _DFS_for_literals_mapping(
        current_node: URIRef | Literal, path_index: int, end_nodes_snapshot: dict
    ) -> int:
        if path_index == metapath.length:
            # logger.debug(f"Found instance end at node: {current_node}")
            if end_nodes_count[current_node] == end_nodes_snapshot[current_node]:
                end_nodes_count[current_node] += 1
            return 0

        number_of_branches = 0

        # Find all nodes that can be the next node in the meta-path instance, based on
        # edge and node type.
        # logger.info(
        #     f"Current relation: {metapath.relations[path_index]}, node:{current_node}"
        # )
        if metapath.reverse_relations[path_index]:
            nodes = (
                s
                for (s, _, _, _) in multigraph.quads(
                    (None, metapath.relations[path_index], current_node, None)
                )
            )
        else:
            nodes = (
                o
                for (_, _, o, _) in multigraph.quads(
                    (current_node, metapath.relations[path_index], None, None)
                )
            )

        for node in nodes:
            if isinstance(node, Literal) and not (
                node.datatype == metapath.node_types[path_index]
                or node.datatype is None
            ):
                # logger.debug(f"At literal: {node.value} - and node.datatype:
                # {node.datatype} and metapath current node type:
                # {metapath.node_types[path_index]}")
                continue
            elif (
                isinstance(node, URIRef)
                and len(
                    list(
                        multigraph.quads(
                            (node, RDF.type, metapath.node_types[path_index], None)
                        )
                    )
                )
                == 0
            ):
                continue
            # logger.debug(f"Current node: {node}")
            number_of_branches += _DFS_for_literals_mapping(
                node, path_index + 1, end_nodes_snapshot
            )

        # Return the number of branches initiated from this node. At least one, even if
        # no instances are found from the current node.
        return max(1, number_of_branches)

    def _DFS(current_node: URIRef | Literal, path_index: int) -> int:
        """Recursive DFS step for finding meta-path instances in a graph. \\
        Parameter path_index indicates the step number of the meta-path traversal. \\
        Traversal is stopped when the index equals the path length, in which case an 
        instance has been found.
        """
        if path_index == metapath.length:
            # logger.info(f"Found instance end at node: {current_node}")
            end_nodes_count[current_node] += 1
            return 0

        number_of_branches = 0

        # Find all nodes that can be the next node in the meta-path instance, based on
        # edge and node type.
        # logger.info(
        #     f"Current relation: {metapath.relations[path_index]}, node:{current_node}"
        # )
        if metapath.reverse_relations[path_index]:
            nodes = (
                s
                for (s, _, _, _) in multigraph.quads(
                    (None, metapath.relations[path_index], current_node, None)
                )
            )
        else:
            nodes = (
                o
                for (_, _, o, _) in multigraph.quads(
                    (current_node, metapath.relations[path_index], None, None)
                )
            )

        snapshot = end_nodes_count.copy()
        for node in nodes:
            if isinstance(node, Literal) and not (
                node.datatype == metapath.node_types[path_index]
                or node.datatype is None
            ):
                # logger.debug(f"At literal: {node.value} - and node.datatype:
                # {node.datatype} and metapath current node type:
                # {metapath.node_types[path_index]}")
                continue
            elif (
                isinstance(node, URIRef)
                and len(
                    list(
                        multigraph.quads(
                            (node, RDF.type, metapath.node_types[path_index], None)
                        )
                    )
                )
                == 0
            ):
                continue
            # logger.info(f"Current node: {node}")
            if metapath.relations[path_index] == QCSM.mapsTo_FAKE:
                number_of_branches = max(
                    1, _DFS_for_literals_mapping(node, path_index + 1, snapshot)
                )
            else:
                number_of_branches += _DFS(node, path_index + 1)

        # Return the number of branches initiated from this node. At least one, even if
        # no instances are found from the current node.
        return max(1, number_of_branches)

    if len(
        list(multigraph.quads((start_node, RDF.type, metapath.start_node_type, None)))
    ) == 0 or (
        isinstance(start_node, Literal) and start_node != metapath.start_node_type
    ):
        logger.error(
            f"Type of start node of meta-path (type {metapath.start_node_type}) does "
            f"not correspond to the type of required start node {start_node}, which is"
            f" {[q for q in multigraph.quads((start_node, RDF.type, metapath.start_node_type, None))]}."
        )
        return dict(), 0

    # A defaultdict will automatically insert non-existing keys when necessary with a
    # default value, here int zero.
    end_nodes_count = defaultdict(int)
    total_branches = _DFS(start_node, 0)
    return dict(end_nodes_count), total_branches


def nodes_with_similarity(
    node_to_compare: URIRef | Literal, metapath: MetaPath, multigraph: RDFDataset
) -> dict[URIRef | Literal, float]:
    counted_instances, number_of_branches = count_instances_by_end_node(
        metapath, node_to_compare, multigraph
    )
    # Apply similarity measure #(path instances)/#(paths initiated),
    # see docs/additional/metapath-based.
    return {
        end_node: number_of_instances / number_of_branches
        for end_node, number_of_instances in counted_instances.items()
    }


def score_composition(
    similarity_scores: dict[UUID, dict[URIRef | Literal, float]],
    metapaths: list[MetaPath],
) -> dict[URIRef | Literal, tuple[float, str]]:
    indexed_metapaths = {path.ID: path for path in metapaths}
    recommendation_with_scores = dict()
    for path_ID, scores in similarity_scores.items():
        path = indexed_metapaths[path_ID]
        for end_node, score in scores.items():
            # logging.info(f"node: {end_node} - score: {score}")
            if end_node not in recommendation_with_scores:
                recommendation_with_scores[end_node] = (
                    score * path.weight,
                    f"Aligns well with your {path.explanation_text}",
                )
            else:
                score_a, explanation_a = recommendation_with_scores[end_node]
                recommendation_with_scores[end_node] = (
                    score_a + score * path.weight,
                    explanation_a + f", {path.explanation_text}",
                )
    return recommendation_with_scores
