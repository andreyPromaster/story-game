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
    graph, root_node = parse_graph(story)
    assert graph == {
        "Root": ["Node1", None],
        "Node1": ["Node2", None],
        "Node2": [None, "Root"],
    }
    assert root_node == "Root"

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_with_unrelated_references.json"
        )
    )
    graph, root_node = parse_graph(story)
    assert graph == {"Root": ["Node1", "Node2", "Node3"]}
    assert root_node == "Root"

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_without_node_options.json"
        )
    )
    graph, root_node = parse_graph(story)
    assert graph == {"Root": ["Node1", "Node2"], "Node1": [], "Node2": []}
    assert root_node == "Root"

    story = parse_story_structure(
        get_test_data_from_json_file(
            "tests/unit/test_json/story_item_changed_default_root_node.json"
        )
    )
    graph, root_node = parse_graph(story)
    assert graph == {"Node1": ["Node2", None], "Node2": [None, None]}
    assert root_node == "Node1"
