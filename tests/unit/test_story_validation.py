import pytest

from data_storage.validators import is_existing_graph_cycle
from tests.test_helpers import not_raises
from utilities.exceptions import ExistsCircleValidationError


def test_not_exist_story_graph_cycle(valid_story_graphs):
    for graph, exit_nodes in valid_story_graphs:
        with not_raises(
            ExistsCircleValidationError,
            f"Graph is {graph}, exit nodes are {exit_nodes}.",
        ):
            breakpoint()
            is_existing_graph_cycle(graph, exit_nodes)


def test_story_has_branch_without_end(cycle_story_graphs):
    breakpoint()
    for graph, exit_nodes in cycle_story_graphs:
        with pytest.raises(ExistsCircleValidationError):
            is_existing_graph_cycle(graph, exit_nodes)
