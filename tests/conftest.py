import json
import os

import boto3
import pytest
from moto import mock_dynamodb2
from sqlalchemy import event
from sqlalchemy.orm import Session

from app import app
from data_storage.dynamo_db.data_source import DynamoDBDriver
from data_storage.sqlalchemy.data_source import RDSDriver
from data_storage.sqlalchemy.models import Base, get_connection


@pytest.fixture(scope="session")
def mock_postgres_creds():
    os.environ["DB_NAME"] = "test"
    os.environ["DB_HOST"] = "127.0.0.1"
    os.environ["DB_PORT"] = "9999"
    os.environ["DB_PASS"] = "testing_password"
    os.environ["DB_USER"] = "testing"


@pytest.fixture(scope="session")
def connection(mock_postgres_creds):
    engine = get_connection()
    connection = engine.connect()

    yield connection

    connection.close()


@pytest.fixture
def mock_rds_driver(connection, setup_db, request):
    """Returns a database session to be used in a test.

    This fixture also alters the application's database
    connection to run in a transactional fashion. This means
    that all tests will run within a transaction, all database
    operations will be rolled back at the end of each test,
    and no test data will be persisted after each test.

    `autouse=True` is used so that session is properly
    initialized at the beginning of the test suite and
    factories can use it automatically.
    """
    transaction = connection.begin()
    session = Session(bind=connection)

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        """Support tests with rollbacks.

        This is required for
         tests that call some services that issue
        rollbacks in try-except blocks.

        With this event the Session always runs all operations within
        the scope of a SAVEPOINT, which is established at the start of
        each transaction, so that tests can also rollback the
        “transaction” as well while still remaining in the scope of a
        larger “transaction” that’s never committed.
        """
        if transaction.nested and not transaction._parent.nested:
            # ensure that state is expired the way session.commit() at
            # the top level normally does
            session.expire_all()
            session.begin_nested()

    def teardown():
        transaction.rollback()

    request.addfinalizer(teardown)

    return RDSDriver(session)


@pytest.fixture
def setup_db(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture
def mock_dynamo_driver(aws_credentials, test_data):
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
