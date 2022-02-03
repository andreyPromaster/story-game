import pytest

from common.entities.schemas import StoryItem
from tests.test_helpers import get_test_data_from_json_file
from utilities.exceptions import ParseGraphError
from utilities.functools import parse_graph, parse_story_structure


def test_parse_story_structure(test_data):
    assert StoryItem(**test_data) == parse_story_structure(test_data)


def test_parse_story_structure_with_invalid_data():
    with pytest.raises(ParseGraphError):
        parse_story_structure(
            get_test_data_from_json_file(
                "tests/unit/test_json/story_without_node_text.json"
            )
        )

    with pytest.raises(ParseGraphError):
        parse_story_structure(
            get_test_data_from_json_file(
                "tests/unit/test_json/story_without_nodes.json"
            )
        )


def test_parse_graph():
    story = parse_story_structure(
        get_test_data_from_json_file("tests/unit/test_json/valid_story.json")
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {
        "Root": ["Node2"],
        "Node1": ["Root"],
        "Node2": ["Node1"],
    }
    assert exit_nodes == {"Root", "Node1", "Node2"}

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_with_unrelated_references.json"
        )
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {
        "Node1": ["Root"],
        "Node2": ["Root"],
        "Node3": ["Root"],
    }
    assert exit_nodes == set()

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_without_node_options.json"
        )
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {"Node1": ["Root"], "Node2": ["Root"]}
    assert exit_nodes == {"Node1", "Node2"}

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_changed_default_root_node.json"
        )
    )
    graph, exit_nodes = parse_graph(story)
    assert graph == {"Node2": ["Node1"]}
    assert exit_nodes == {"Node1", "Node2"}
