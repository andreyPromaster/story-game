import json
import logging
from functools import partial

from pydantic.json import pydantic_encoder
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from conf import settings


def get_connection():
    # Setup Session and Client
    logging.info("Getting database connection")
    conn = create_engine(
        f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
        json_serializer=partial(json.dumps, default=pydantic_encoder),
    )
    logging.info("Database connection established")
    return conn


engine = get_connection()
Base = declarative_base(bind=engine)


class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True)
    story = Column(
        Integer,
        ForeignKey("story.id", ondelete="CASCADE"),
        nullable=True,
    )
    name = Column(String(200), nullable=False, index=True)
    text = Column(String(200), nullable=False)


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    next = Column(
        Integer, ForeignKey("node.id", ondelete="CASCADE"), nullable=True, index=True
    )
    cur_node = Column(Integer, ForeignKey("node.id", ondelete="CASCADE"), index=True)
    text = Column(String(200), nullable=False)
