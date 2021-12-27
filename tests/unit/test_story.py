from unittest.mock import MagicMock

import pytest

from common.entities.schemas import Node
from utilities.exceptions import DynamoDBError


@pytest.mark.parametrize(
    "db_driver", ["mock_dynamo_driver", "mock_rds_driver"], indirect=True
)
def test_get_story(db_driver, test_data):
    story = db_driver.get_story("1")
    assert story.id == test_data["id"]
    assert story.root == test_data["root"]


@pytest.mark.parametrize(
    "db_driver", ["mock_dynamo_driver", "mock_rds_driver"], indirect=True
)
def test_get_not_exist_story(db_driver):
    story = db_driver.get_story("not_exist_id")
    assert story is None


def test_get_story_with_response_error(mock_dynamo_driver):
    mock_dynamo_driver.connection = MagicMock()
    mock_dynamo_driver.connection.query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 404}
    }
    with pytest.raises(DynamoDBError):
        mock_dynamo_driver.get_story("not_exist_id")


@pytest.mark.parametrize(
    "db_driver", ["mock_dynamo_driver", "mock_rds_driver"], indirect=True
)
def test_get_node(db_driver, test_data):
    node = db_driver.get_node("1", "Root")
    assert Node(**test_data["nodes"]["Root"]) == node


@pytest.mark.parametrize(
    "db_driver", ["mock_dynamo_driver", "mock_rds_driver"], indirect=True
)
def test_get_not_exist_node(db_driver):
    node = db_driver.get_node("1", "not_exist_id")
    assert node is None
