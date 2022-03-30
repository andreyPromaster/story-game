import pytest

from common.entities.schemas import StoryItem
from tests.constants import PARSED_STORY_GRAPH, PARSED_STORY_GRAPH_AS_INCIDENCE_MATRIX
from tests.helpers import load_json
from utilities.exceptions import ParseGraphError
from utilities.functools import (
    parse_graph,
    parse_graph_as_incidence_matrix,
    parse_story_structure,
)


def test_parse_story_structure(test_data):
    assert StoryItem(**test_data) == parse_story_structure(test_data)


@pytest.mark.parametrize(
    "test_story_file",
    [
        "tests/unit/test_json/story_without_node_text.json",
        "tests/unit/test_json/story_without_nodes.json",
    ],
)
def test_parse_story_structure_with_invalid_data(test_story_file):
    with pytest.raises(ParseGraphError):
        parse_story_structure(load_json(test_story_file))


@pytest.mark.parametrize(
    "test_json, expected_graph, expected_exit_nodes", PARSED_STORY_GRAPH
)
def test_parse_graph(test_json, expected_graph, expected_exit_nodes):
    story = parse_story_structure(load_json(test_json))
    graph, exit_nodes = parse_graph(story)
    assert graph == expected_graph
    assert exit_nodes == expected_exit_nodes


@pytest.mark.parametrize(
    "test_json, expected_graph", PARSED_STORY_GRAPH_AS_INCIDENCE_MATRIX
)
def test_parse_graph_as_incidence_matrix(test_json, expected_graph):
    story = parse_story_structure(load_json(test_json))
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == expected_graph
