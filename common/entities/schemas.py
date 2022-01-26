from typing import Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field, validator


def generate_uuid_as_str():
    return str(uuid4())


class Option(BaseModel):
    text: str
    next: str = None


class Node(BaseModel):
    options: List[Option] = []
    text: str

    class Config:
        orm_mode = True


class NodeList(BaseModel):
    nodes: Dict[str, Node]


class Story(BaseModel):
    id: str
    root: str = "Root"
    name: str

    @validator("id")
    def username_alphanumeric(cls, v):
        UUID_LENGTH = 36
        assert len(v) < UUID_LENGTH, "length must be less than 36 symbols"
        return v

    class Config:
        orm_mode = True


class StoryItem(Story, NodeList):
    id: str = Field(default_factory=generate_uuid_as_str)


class StoryList(BaseModel):
    stories: List[Story] = []

    class Config:
        orm_mode = True
