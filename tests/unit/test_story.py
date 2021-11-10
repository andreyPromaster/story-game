from unittest.mock import MagicMock

import pytest

from entities.schemas import Node
from utilities.exceptions import DynamoDBError


def test_get_story(mock_db_session, test_data):
    story = mock_db_session.get_story("test_id")
    print(story.id, test_data)
    assert story.id == test_data["id"]
    assert story.root == test_data["root"]

def test_get_not_exist_story(mock_db_session):
    story = mock_db_session.get_story("not_exist_id")
    assert story is None

def test_get_story_with_response_error(mock_db_session):
    mock_db_session.connection = MagicMock()
    mock_db_session.connection.query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 404}
    }
    with pytest.raises(DynamoDBError):
        mock_db_session.get_story("test_id")

def test_get_node(mock_db_session, test_data):
    node = mock_db_session.get_node("test_id", "Root")
    assert Node(**test_data["nodes"]["Root"]) == node

def test_get_not_exist_node(mock_db_session):
    node = mock_db_session.get_node("test_id", "not_exist_id")
    assert node is None
