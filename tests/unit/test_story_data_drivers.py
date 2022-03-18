from unittest.mock import MagicMock

import pytest
from boto3.dynamodb.conditions import Key

from common.entities.schemas import Node
from data_storage.sqlalchemy import models
from tests.test_helpers import get_test_data_from_json_file
from utilities.exceptions import DynamoDBError, ValidationError


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
def test_get_story(data_driver, test_data):
    story = data_driver.get_story("1")
    assert story.id == test_data["id"]
    assert story.root == test_data["root"]
    assert story.name == test_data["name"]


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
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


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
def test_get_node(data_driver, test_data):
    node = data_driver.get_node("1", "Root")
    assert Node(**test_data["nodes"]["Root"]) == node


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
def test_get_not_exist_node(data_driver):
    node = data_driver.get_node("1", "not_exist_id")
    assert node is None


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
def test_get_story_list(data_driver, test_data):
    stories = data_driver.get_story_list()
    assert stories.stories[0].id == test_data["id"]
    assert stories.stories[0].root == test_data["root"]
    assert stories.stories[0].name == test_data["name"]


def test_create_story_dynamodb_driver(mock_dynamodb_driver):
    story_data = get_test_data_from_json_file(
        "tests/integration/test_json/valid_story_item.json"
    )
    story = mock_dynamodb_driver.create_story(story_data)
    assert story.id is not None
    assert story.root == story_data["root"]
    assert story.name == story_data["name"]
    response = mock_dynamodb_driver.connection.query(
        KeyConditionExpression=Key("id").eq(story.id)
    )
    assert response["Items"][0] == story.dict()


def test_create_story_rds_driver(mock_rds_driver):
    story_data = get_test_data_from_json_file(
        "tests/integration/test_json/valid_story_item.json"
    )
    story = mock_rds_driver.create_story(story_data)
    assert story.id is not None
    assert story.root == story_data["root"]
    assert story.name == story_data["name"]
    story_rds = (
        mock_rds_driver.session.query(models.Story)
        .filter(models.Story.id == story.id)
        .one()
    )

    assert story_rds.name == story_data["name"]
    story_nodes_rds = (
        mock_rds_driver.session.query(Node)
        .filter(models.Node.story == story.id)
        .all()
        .join(models.Node, models.Option.cur_node == Node.id, isouter=True)
    )
    assert len(story_nodes_rds) == 4


@pytest.mark.parametrize(
    "data_driver", ["mock_dynamodb_driver", "mock_rds_driver"], indirect=True
)
def test_create_failed_story(data_driver):
    story_data = get_test_data_from_json_file(
        "tests/integration/test_json/invalid_story_item_with_circle.json"
    )
    with pytest.raises(ValidationError):
        data_driver.create_story(story_data)
