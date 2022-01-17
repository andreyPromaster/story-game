from typing import Dict, List, Optional

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
    nodes: Dict[str, Node]


class Story(BaseModel):
    id: str
    root: str = "Root"
    name: Optional[str]

    class Config:
        orm_mode = True


class StoryItem(Story, NodeList):
    id: Optional[str]


class StoryList(BaseModel):
    stories: List[Story] = []

    class Config:
        orm_mode = True
