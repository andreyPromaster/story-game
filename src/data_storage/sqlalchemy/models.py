import json
import logging
from functools import partial

from pydantic.json import pydantic_encoder
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(bind=engine)


class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    root = Column(
        Integer,
        ForeignKey("node.id", ondelete="CASCADE", use_alter=True),
        nullable=False,
        index=True,
    )
    name = Column(VARCHAR(200), nullable=False)


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True)
    story = Column(
        Integer,
        ForeignKey("story.id", ondelete="CASCADE", use_alter=True),
        nullable=False,
        index=True,
    )
    name = Column(VARCHAR(200), nullable=False)
    text = Column(VARCHAR(200), nullable=False)


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    next = Column(
        Integer, ForeignKey("node.id", ondelete="CASCADE"), nullable=False, index=True
    )
    text = Column(VARCHAR(200), nullable=False)