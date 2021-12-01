from typing import List, Optional

from pydantic import BaseModel


class Option(BaseModel):
    text: str
    next: str = None


class Node(BaseModel):
    options: List[Option] = []
    text: str

    class Config:
        orm_mode = True


class NodeList(BaseModel):
    nodes: List[Node] = []


class Story(BaseModel):
    id: str
    root: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True


class StoryList(BaseModel):
    stories: List[Story] = []

    class Config:
        orm_mode = True
