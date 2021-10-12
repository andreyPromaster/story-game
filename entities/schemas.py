from typing import List

from pydantic import BaseModel


class Option(BaseModel):
    text: str
    next: str


class Node(BaseModel):
    options: List[Option] = []
    text: str


class NodeList(BaseModel):
    nodes: List[Node] = []
