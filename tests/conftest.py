import json
import os

import boto3
import pytest
from moto import mock_dynamodb2

from app import app
from data_storage.data_source import DynamoDBDriver


@pytest.fixture
def mock_db_session(aws_credentials, test_data):
    mock_dynamodb = mock_dynamodb2()
    mock_dynamodb.start()
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
    client.Table(TABLE_NAME).put_item(Item=test_data)
    yield DynamoDBDriver(client)
    mock_dynamodb.stop()


@pytest.fixture
def application_client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def test_data():
    with open("tests/test_data.json", "r") as file:
        test_data = json.load(file)
        return test_data


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
