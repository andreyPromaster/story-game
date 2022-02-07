from typing import DefaultDict

from common.entities.schemas import StoryItem
from utilities.exceptions import (
    ExistsCircleValidationError,
    RootDoesNotExistValidationError,
    UnconnectedNodeValidationError,
    UnrelatedReferenceValidationError,
)


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

    if set(graph.keys()) != has_exit:
        raise ExistsCircleValidationError


def is_existing_root_node(story_data: StoryItem):
    if story_data.root not in story_data.nodes.keys():
        raise RootDoesNotExistValidationError(
            f"Provided {story_data.root} root node does not exist"
        )


def is_existing_unconnected_node(graph, root_node, exit_nodes: set):
    """Root is one possible node that does not have any references"""
    is_valid = any((node or key == root_node) for key, node in graph.items())
    if not is_valid:
        raise UnconnectedNodeValidationError
    elif not exit_nodes.issubset(graph.keys()):
        raise UnconnectedNodeValidationError


def is_existing_unrelated_reference(graph):
    nodes = set(graph.keys())
    unique_references = set()
    for references in graph.values():
        for reference in references:
            unique_references.add(reference)

    if nodes != unique_references:
        raise UnrelatedReferenceValidationError
