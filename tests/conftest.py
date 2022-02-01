import json
import os
from unittest import mock

import boto3
import pytest
from moto import mock_dynamodb2
from sqlalchemy import event, text
from sqlalchemy.orm import Session

from app import app
from data_storage.dynamo_db.data_source import DynamoDBDriver
from data_storage.sqlalchemy.data_source import RDSDriver
from data_storage.sqlalchemy.models import Base, get_connection_engine


@pytest.fixture(scope="session")
def mock_postgres_creds():
    test_env = {
        **os.environ,
        "DB_NAME": "test",
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "9999",
        "DB_PASS": "testing_password",
        "DB_USER": "testing",
    }
    with mock.patch("os.environ", test_env):
        yield


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


def load_test_sql_data(connection):
    with open("tests/test_data.sql") as file:
        query = text(file.read())
        connection.execute(query)


@pytest.fixture(scope="session")
def test_data():
    with open("tests/test_data.json", "r") as file:
        test_data = json.load(file)
    return test_data


@pytest.fixture(scope="session")
def engine(mock_postgres_creds):
    return get_connection_engine()


@pytest.fixture
def data_driver(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def mock_rds_driver(engine, setup_db, request):
    connection = engine.connect()

    load_test_sql_data(connection)

    transaction = connection.begin()
    session = Session(bind=connection)

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)

    return RDSDriver(session)


@pytest.fixture
def setup_db(engine):
    connection = engine.connect()
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture
def mock_dynamodb_driver(aws_credentials, test_data):
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
    yield DynamoDBDriver(client.Table(TABLE_NAME))
    mock_dynamodb.stop()


@pytest.fixture
def application_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_story_graphs():
    data = (
        (
            {
                "Root": [None, "Node1"],
                "Node1": ["Root"],
            },
            "Root",
        ),
        (
            {
                "Root": ["Node1"],
                "Node1": ["Root", None],
            },
            "Root",
        ),
        (
            {
                "Root": ["Node1"],
                "Node1": ["Root", None],
            },
            "Root",
        ),
        (
            {
                "Node1": ["Node2", "Node3", "Node4"],
                "Node2": ["Node3", None],
                "Node3": ["Node4"],
                "Node4": [],
            },
            "Node1",
        ),
        (
            {
                "Node1": ["Node2", "Node3"],
                "Node2": ["Node1", "Node4"],
                "Node3": ["Node4", "Node5"],
                "Node4": ["Node6"],
                "Node5": [],
                "Node6": ["Node2"],
            },
            "Node1",
        ),
    )
    return data


@pytest.fixture
def cycle_story_graphs():
    data = (
        (
            {
                "Root": ["Node1"],
                "Node1": ["Node2"],
                "Node2": ["Node1"],
            },
            "Root",
        ),
        (
            {
                "Node1": ["Node2", "Node3"],
                "Node2": ["Node1", "Node4"],
                "Node3": ["Node4", "Node5"],
                "Node4": ["Node6"],
                "Node5": ["Node3"],
                "Node6": ["Node2"],
            },
            "Node1",
        ),
        (
            {
                "Node1": ["Node2", "Node3"],
                "Node2": ["Node5", "Node6"],
                "Node3": ["Node4", "Node5"],
                "Node4": ["Node5", "Node3"],
                "Node5": ["Node3", "Node4"],
                "Node6": [],
            },
            "Node1",
        ),
    )
    return data
