from unittest.mock import MagicMock

import pytest

from common.entities.schemas import Node
from utilities.exceptions import DynamoDBError


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
