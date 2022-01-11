import json
import logging
from functools import partial

from pydantic.json import pydantic_encoder
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from conf import RDSSettings


def get_connection_engine():
    # Setup Session and Client
    logging.info("Getting database connection")
    rds_setting = RDSSettings()
    conn = create_engine(
        f"postgresql://{rds_setting.DB_USER}:{rds_setting.DB_PASS}@"
        f"{rds_setting.DB_HOST}:{rds_setting.DB_PORT}/{rds_setting.DB_NAME}",
        json_serializer=partial(json.dumps, default=pydantic_encoder),
    )
    logging.info("Database connection established")
    return conn


# TO DO: make lazy connection
engine = get_connection_engine()
Base = declarative_base(bind=engine)


class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)


class Node(Base):
    """Make boolean flag to show root node or name always root node as Root"""
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
