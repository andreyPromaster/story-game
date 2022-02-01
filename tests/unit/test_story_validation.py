import pytest

from data_storage.validators import is_existing_graph_cycle
from tests.test_helpers import not_raises
from utilities.exceptions import ExistsCircleValidationError


def test_not_exist_story_graph_cycle(valid_story_graphs):
    for graph, root_node in valid_story_graphs:
        with not_raises(
            ExistsCircleValidationError, f"Graph is {graph}, root node is {root_node}."
        ):
            is_existing_graph_cycle(graph, root_node)


def test_story_has_branch_without_end(cycle_story_graphs):
    breakpoint()
    for graph, root_node in cycle_story_graphs:
        with pytest.raises(ExistsCircleValidationError):
            is_existing_graph_cycle(graph, root_node)
