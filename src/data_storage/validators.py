from utilities.exceptions import (
    ExistsCircleValidationError,
    RootDoesNotExistValidationError,
    UnconnectedNodeValidationError,
    UnrelatedReferenceValidationError,
)


def deep_first_search(graph, current_vertex, color={}):
    if current_vertex is None:
        return False
    color[current_vertex] = "grey"

    circle_result = []
    for node in graph[current_vertex]:
        node_color = color.get(node)
        if node_color is None:  # it is expected that all nodes have white color
            circle_result.append(deep_first_search(graph, node, color))
        if node_color == "grey":
            return True

    color[current_vertex] = "black"
    return all(circle_result)


def is_existing_graph_cycle(graph):
    if deep_first_search(graph, "Root"):
        raise ExistsCircleValidationError


def is_existing_root_node(graph):
    if "Root" not in graph.keys():
        raise RootDoesNotExistValidationError


def is_existing_unconnected_node(graph):
    for key, references in graph.items():
        if key not in references:
            raise UnconnectedNodeValidationError


def is_existing_unrelated_reference(graph):
    """Use sets, not lists"""
    for references in graph.values():
        for reference in references:
            if reference not in graph.key():
                raise UnrelatedReferenceValidationError
