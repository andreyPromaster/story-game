import pytest

from common.entities.schemas import StoryItem
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


def test_parse_graph():
    story = parse_story_structure(load_json("tests/unit/test_json/valid_story.json"))
    graph, exit_nodes = parse_graph(story)
    assert graph == {
        "Root": ["Node2"],
        "Node1": ["Root"],
        "Node2": ["Node1"],
    }
    assert exit_nodes == {"Root", "Node1", "Node2"}

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_unrelated_references.json")
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {
        "Node1": ["Root"],
        "Node2": ["Root"],
        "Node3": ["Root"],
    }
    assert exit_nodes == set()

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_without_node_options.json")
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {"Node1": ["Root"], "Node2": ["Root"]}
    assert exit_nodes == {"Node1", "Node2"}

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_changed_default_root_node.json")
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {"Node2": ["Node1"]}
    assert exit_nodes == {"Node1", "Node2"}


def test_parse_graph_as_incidence_matrix():
    story = parse_story_structure(load_json("tests/unit/test_json/valid_story.json"))
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == {
        "Root": ["Node1", None],
        "Node1": ["Node2", None],
        "Node2": [None, "Root"],
    }

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_unrelated_references.json")
    )
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == {
        "Root": ["Node1", "Node2", "Node3"],
    }

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_without_node_options.json")
    )
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == {
        "Root": ["Node1", "Node2"],
        "Node1": [],
        "Node2": [],
    }

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_changed_default_root_node.json")
    )
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == {
        "Node1": ["Node2", None],
        "Node2": [None, None],
    }

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_group_unconnected_nodes.json")
    )
    graph = parse_graph_as_incidence_matrix(story)
    assert graph == {
        "Root": [None, "Root1"],
        "Root1": [None, None],
        "Node1": ["Node2"],
        "Node2": ["Node3"],
        "Node3": ["Node1", None],
    }
