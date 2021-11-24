from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

from data_storage.sqlalchemy.data_source import get_connection

engine = get_connection()
Base = declarative_base(bind=engine)


class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(200), nullable=False)


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True)
    story = Column(
        Integer,
        ForeignKey("story.id", ondelete="CASCADE"),
        nullable=True,
    )
    name = Column(VARCHAR(200), nullable=False, index=True)
    text = Column(VARCHAR(200), nullable=False)


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    next = Column(
        Integer, ForeignKey("node.id", ondelete="CASCADE"), nullable=True, index=True
    )
    cur_node = Column(Integer, ForeignKey("node.id", ondelete="CASCADE"), index=True)
    text = Column(VARCHAR(200), nullable=False)
