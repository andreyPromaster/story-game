from typing import DefaultDict

from common.entities.schemas import StoryItem
from utilities.exceptions import (
    ExistsCircleValidationError,
    RootDoesNotExistValidationError,
    UnconnectedNodeValidationError,
    UnrelatedReferenceValidationError,
)
from utilities.functools import parse_graph_as_incidence_matrix


def is_existing_graph_cycle(graph: DefaultDict[str, list], exit_nodes: set):
    """
    The basic idea is to start from node that has reference to None
    or has no options(exit_node) and mark the node(that has exit and move)
    to the adjacent unmarked node and continue this loop
    until there is no unmarked adjacent node.

    If we have unmarked node that means story has branch without end.
    """

    has_exit = set()

    def deep_first_search(current_vertex):

        has_exit.add(current_vertex)

        for node in graph[current_vertex]:
            if node not in has_exit:
                deep_first_search(node)

    for exit_node in exit_nodes:
        deep_first_search(exit_node)

    if graph.keys() != has_exit:
        raise ExistsCircleValidationError


def is_existing_root_node(story_data: StoryItem):
    if story_data.root not in story_data.nodes.keys():
        raise RootDoesNotExistValidationError(
            f"Provided {story_data.root} root node does not exist"
        )


def is_existing_disconnected_graph_components(story_item: StoryItem):
    graph = parse_graph_as_incidence_matrix(story_item)
    visited = set()

    def dfs(node):
        visited.add(node)
        references = graph.get(node)

        if references is None:
            raise UnrelatedReferenceValidationError

        for reference in references:
            if reference not in visited and reference is not None:
                dfs(reference)

    dfs(story_item.root)

    if graph.keys() != visited:
        raise UnconnectedNodeValidationError
