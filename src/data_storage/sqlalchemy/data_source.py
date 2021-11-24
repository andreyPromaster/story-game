import json
import logging
from functools import partial, wraps

from pydantic.json import pydantic_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf import settings
from data_storage.data_source import DataDriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def execute_query(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        with self.session() as db:
            with db.begin():
                return method(self, *args, **kwargs)

    return inner


def get_connection():
    # Setup Session and Client
    logging.info("Getting database connection")
    conn = create_engine(
        f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
        json_serializer=partial(json.dumps, default=pydantic_encoder),
    )
    logging.info("Database connection established")
    return conn


class RDSDriver(DataDriver):
    def __init__(self, session=None):
        if session is None:
            engine = get_connection()
            self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        else:
            self.session = session

    @execute_query
    def get_story(self, story_id: str):
        raise NotImplementedError

    @execute_query
    def get_node(self, story_id: str, uri: str):
        raise NotImplementedError

    @execute_query
    def get_story_list(self):
        raise NotImplementedError
