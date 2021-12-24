from unittest.mock import MagicMock

import pytest

from common.entities.schemas import Node
from utilities.exceptions import DynamoDBError


def test_get_story(mock_rds_driver, test_data):
    story = mock_rds_driver.get_story("test_id")
    assert story.id == test_data["id"]
    assert story.root == test_data["root"]


def test_get_not_exist_story(mock_dynamo_driver):
    story = mock_dynamo_driver.get_story("not_exist_id")
    assert story is None


def test_get_story_with_response_error(mock_dynamo_driver):
    mock_dynamo_driver.connection = MagicMock()
    mock_dynamo_driver.connection.query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 404}
    }
    with pytest.raises(DynamoDBError):
        mock_dynamo_driver.get_story("test_id")


def test_get_node(mock_dynamo_driver, test_data):
    node = mock_dynamo_driver.get_node("test_id", "Root")
    assert Node(**test_data["nodes"]["Root"]) == node


def test_get_not_exist_node(mock_dynamo_driver):
    node = mock_dynamo_driver.get_node("test_id", "not_exist_id")
    assert node is None
