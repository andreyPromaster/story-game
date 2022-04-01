from unittest.mock import MagicMock

import pytest
from boto3.dynamodb.conditions import Key

from common.entities.schemas import Node
from data_storage.sqlalchemy import models
from tests.helpers import load_json
from utilities.exceptions import DynamoDBError, ValidationError

DEFAULT_DRIVERS = ["mock_dynamodb_driver", "mock_rds_driver"]


def with_drivers(drivers):
    return pytest.mark.parametrize("data_driver", drivers, indirect=True)


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_get_story(data_driver, test_data):
    story = data_driver.get_story("1")
    assert story.id == test_data["id"]
    assert story.root == test_data["root"]
    assert story.name == test_data["name"]


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_get_not_exist_story(data_driver):
    story = data_driver.get_story("not_exist_id")
    assert story is None


def test_get_story_with_response_error(mock_dynamodb_driver):
    mock_dynamodb_driver.connection = MagicMock()
    mock_dynamodb_driver.connection.query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 404}
    }
    with pytest.raises(DynamoDBError):
        mock_dynamodb_driver.get_story("not_exist_id")


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_get_node(data_driver, test_data):
    node = data_driver.get_node("1", "Root")
    assert Node(**test_data["nodes"]["Root"]) == node


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_get_not_exist_node(data_driver):
    node = data_driver.get_node("1", "not_exist_id")
    assert node is None


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_get_story_list(data_driver, test_data):
    stories = data_driver.get_story_list()
    assert len(stories.stories) == 1
    assert stories.stories[0].id == test_data["id"]
    assert stories.stories[0].root == test_data["root"]
    assert stories.stories[0].name == test_data["name"]


def test_create_story_dynamodb_driver(mock_dynamodb_driver):
    story_data = load_json("tests/data/valid_story_item.json")
    story = mock_dynamodb_driver.create_story(story_data)
    assert story.id is not None
    assert story.root == story_data["root"]
    assert story.name == story_data["name"]
    response = mock_dynamodb_driver.connection.query(
        KeyConditionExpression=Key("id").eq(story.id)
    )
    assert response["Items"][0] == story.dict()


def test_create_story_rds_driver(mock_rds_driver):
    story_data = load_json("tests/data/valid_story_item.json")
    story = mock_rds_driver.create_story(story_data)
    assert story.id is not None
    assert story.root == story_data["root"]
    assert story.name == story_data["name"]
    story_rds = (
        mock_rds_driver.session.query(models.Story)
        .filter(models.Story.id == story.id)
        .one()
    )
    assert story_rds.id == story.id
    assert story_rds.name == story_data["name"]
    story_nodes_rds = (
        mock_rds_driver.session.query(models.Node)
        .filter(models.Node.story == story.id)
        .all()
    )
    assert len(story_nodes_rds) == 4

    сount_story_options_rds = (
        mock_rds_driver.session.query(models.Option)
        .filter(
            models.Option.cur_node.in_(list(map(lambda node: node.id, story_nodes_rds)))
        )
        .count()
    )
    assert сount_story_options_rds == 7


@with_drivers(drivers=DEFAULT_DRIVERS)
def test_create_failed_story(data_driver):
    story_data = load_json("tests/data/invalid_story_item_with_circle.json")
    with pytest.raises(ValidationError):
        data_driver.create_story(story_data)
