import pytest

from data_storage.data_source import DataDriver
from data_storage.validators import is_existing_graph_cycle
from tests.constants import CYCLE_STORY_GRAPHS, VALID_STORY_ITEM
from tests.helpers import load_json, not_raises
from utilities.exceptions import (
    ExistsCircleValidationError,
    RootDoesNotExistValidationError,
    UnconnectedNodeValidationError,
    UnrelatedReferenceValidationError,
    ValidationError,
)
from utilities.functools import parse_story_structure


def test_not_exist_story_graph_cycle():
    for graph, exit_nodes in VALID_STORY_ITEM:
        with not_raises(
            ExistsCircleValidationError,
            f"Graph is {graph}, exit nodes are {exit_nodes}.",
        ):
            is_existing_graph_cycle(graph, exit_nodes)


def test_story_has_branch_without_end():
    for graph, exit_nodes in CYCLE_STORY_GRAPHS:
        with pytest.raises(ExistsCircleValidationError):
            is_existing_graph_cycle(graph, exit_nodes)


def test_validate_story_item():
    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_unrelated_references.json")
    )
    with pytest.raises(UnrelatedReferenceValidationError):
        DataDriver.validate_story_item(story)

    story = parse_story_structure(load_json("tests/unit/test_json/valid_story.json"))
    with not_raises(ValidationError):
        DataDriver.validate_story_item(story)

    story = parse_story_structure(
        load_json("tests/unit/test_json/valid_story_item.json")
    )
    with not_raises(ValidationError):
        DataDriver.validate_story_item(story)

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_without_root_node.json")
    )
    with pytest.raises(RootDoesNotExistValidationError):
        DataDriver.validate_story_item(story)
    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_unconnected_node.json")
    )
    with pytest.raises(UnconnectedNodeValidationError):
        DataDriver.validate_story_item(story)

    story = parse_story_structure(
        load_json("tests/unit/test_json/story_item_with_group_unconnected_nodes.json")
    )
    with pytest.raises(UnconnectedNodeValidationError):
        DataDriver.validate_story_item(story)
