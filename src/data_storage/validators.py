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


# FIX ME
def is_existing_unconnected_node(graph, parsed_nodes, root_node):
    """Алгоритм проверки связности графа G"""
    referred_nodes = graph.keys()
    for node in parsed_nodes:
        if node not in referred_nodes and node != root_node:
            raise UnconnectedNodeValidationError


def is_existing_unrelated_reference(graph, nodes):
    nodes = set(nodes)
    unique_references = set()
    for references in graph.values():
        unique_references.update(references)

    if not unique_references.issubset(nodes):
        raise UnrelatedReferenceValidationError
