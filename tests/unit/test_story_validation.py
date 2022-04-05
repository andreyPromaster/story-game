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
    for story_item in VALID_STORY_ITEM:
        with not_raises(
            ExistsCircleValidationError,
            f"Graph is {story_item['graph']}, exit nodes are {story_item['exit_nodes']}.",
        ):
            is_existing_graph_cycle(story_item["graph"], story_item["exit_nodes"])


def test_story_has_branch_without_end():
    for story_item in CYCLE_STORY_GRAPHS:
        with pytest.raises(ExistsCircleValidationError):
            is_existing_graph_cycle(story_item["graph"], story_item["exit_nodes"])


@pytest.mark.parametrize(
    "test_data_json",
    [
        "tests/unit/test_json/story_item_with_unrelated_references.json",
    ],
)
def test_validate_story_item_with_unrelated_reference(test_data_json):
    story = parse_story_structure(load_json(test_data_json))
    with pytest.raises(UnrelatedReferenceValidationError):
        DataDriver.validate_story_item(story)


@pytest.mark.parametrize(
    "test_data_json",
    [
        "tests/unit/test_json/valid_story.json",
        "tests/unit/test_json/valid_story_item.json",
    ],
)
def test_validate_story_item(test_data_json):
    story = parse_story_structure(load_json(test_data_json))
    with not_raises(ValidationError):
        DataDriver.validate_story_item(story)


@pytest.mark.parametrize(
    "test_data_json",
    [
        "tests/unit/test_json/story_item_without_root_node.json",
    ],
)
def test_validate_story_item_without_root_node(test_data_json):
    story = parse_story_structure(load_json(test_data_json))
    with pytest.raises(RootDoesNotExistValidationError):
        DataDriver.validate_story_item(story)


@pytest.mark.parametrize(
    "test_data_json",
    [
        "tests/unit/test_json/story_item_with_unconnected_node.json",
        "tests/unit/test_json/story_item_with_group_unconnected_nodes.json",
    ],
)
def test_validate_story_item_with_unconnected_node(test_data_json):
    story = parse_story_structure(load_json(test_data_json))
    with pytest.raises(UnconnectedNodeValidationError):
        DataDriver.validate_story_item(story)
