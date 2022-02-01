from itertools import chain

from utilities.exceptions import (
    ExistsCircleValidationError,
    RootDoesNotExistValidationError,
    UnconnectedNodeValidationError,
    UnrelatedReferenceValidationError,
)


def deep_first_search(graph, current_vertex, color=None):
    if color is None:
        color = {}

    # If we have reference to None or node without options it means branch has end
    if current_vertex is None or not graph[current_vertex]:
        return False
    color[current_vertex] = "grey"

    circle_result = []
    for node in graph[current_vertex]:
        node_color = color.get(node)
        if node_color is None:  # it is expected that all nodes have white color
            circle_result.append(deep_first_search(graph, node, color))
        if node_color == "grey":
            circle_result.append(True)

    color[current_vertex] = "black"
    return all(circle_result)


def is_existing_graph_cycle(graph, root_node):
    """This  validation will run after def is_existing_root_node"""
    if deep_first_search(graph, root_node):
        raise ExistsCircleValidationError


def is_existing_root_node(graph, root_node):
    if root_node not in graph.keys():
        raise RootDoesNotExistValidationError(
            f"Provided {root_node} root node does not exist"
        )


def is_existing_unconnected_node(graph, root_node):
    """Root is one possible node that does not have any references"""
    references = set(chain.from_iterable(graph.values()))
    for node in graph.keys():
        if node not in references and node != root_node:
            raise UnconnectedNodeValidationError


def is_existing_unrelated_reference(graph):
    nodes = set(graph.keys())

    for references in graph.values():
        for reference in references:
            if reference not in nodes and reference is not None:
                raise UnrelatedReferenceValidationError
