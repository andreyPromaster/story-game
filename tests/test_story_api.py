import json
import os
import unittest
from unittest.mock import MagicMock, patch

import boto3
from moto import mock_dynamodb2

from app import app
from entities.data_source import DynamoDBDriver
from entities.schemas import Node
from utilities.exceptions import DynamoDBError


@patch.dict(
    os.environ,
    {
        "AWS_ACCESS_KEY_ID": "testing",
        "AWS_SECRET_ACCESS_KEY": "testing",
        "AWS_SECURITY_TOKEN": "testing",
        "AWS_SESSION_TOKEN": "testing",
    },
    clear=True,
)
class StoryDynamoDBTest(unittest.TestCase):
    mock_dynamodb = mock_dynamodb2()
    TABLE_NAME = os.getenv("STORY_TABLE_NAME", "stories")

    def setUp(self):
        self.mock_dynamodb.start()
        boto3.setup_default_session()
        self.client = boto3.resource(
            "dynamodb", region_name=os.getenv("REGION", "us-east-1")
        )
        self.client.create_table(
            TableName=self.TABLE_NAME,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
        )
        with open("tests/test_data.json", "r") as file:
            self.test_data = json.load(file)
        self.client.Table(self.TABLE_NAME).put_item(Item=self.test_data)
        self.story_data_source = DynamoDBDriver(self.client)
        self.app = app.test_client()

    def tearDown(self):
        self.mock_dynamodb.stop()

    def test_get_story(self):
        story = self.story_data_source.get_story("test_id")
        assert story.id == self.test_data["id"]
        assert story.root == self.test_data["root"]

    def test_get_not_exist_story(self):
        story = self.story_data_source.get_story("not_exist_id")
        self.assertIsNone(story)

    def test_get_story_with_response_error(self):
        self.story_data_source.connection = MagicMock()
        self.story_data_source.connection.query.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 404}
        }
        with self.assertRaises(DynamoDBError):
            self.story_data_source.get_story("test_id")

    def test_get_node(self):
        node = self.story_data_source.get_node("test_id", "Root")
        assert Node(**self.test_data["nodes"]["Root"]) == node

    def test_get_not_exist_node(self):
        node = self.story_data_source.get_node("test_id", "not_exist_id")
        self.assertIsNone(node)

    @patch("entities.data_source.get_data_source")
    def test_get_story_list(self, mocker):
        mocker.return_value = self.client
        data = self.app.get("api/story")
        assert data.status_code == 200
        assert data.get_json() == {
            key: value for key, value in self.test_data.items() if key in ("id", "root")
        }
