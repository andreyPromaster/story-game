import json
import os

import boto3
import pytest
from moto import mock_dynamodb2

from app import app
from entities.data_source import DynamoDBDriver


@pytest.fixture()
def mock_db_session():
    mock_dynamodb = mock_dynamodb2()
    mock_dynamodb.start()
    boto3.setup_default_session()
    TABLE_NAME = os.getenv("STORY_TABLE_NAME", "stories")
    client = boto3.resource("dynamodb", region_name=os.getenv("REGION", "us-east-1"))
    client.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
        ],
    )
    with open("tests/test_data.json", "r") as file:
        test_data = json.load(file)
    client.Table(TABLE_NAME).put_item(Item=test_data)
    yield DynamoDBDriver(client)
    mock_dynamodb.stop()


@pytest.fixture(scope="session")
def application_client():
    return app.test_client()


@pytest.fixture(scope="session", autouse=True)
def test_data():
    with open("tests/test_data.json", "r") as file:
        test_data = json.load(file)
        return test_data
