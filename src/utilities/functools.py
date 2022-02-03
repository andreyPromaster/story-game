from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict

from pydantic import ValidationError

from common.entities.schemas import StoryItem
from utilities.exceptions import ParseGraphError


def parse_story_structure(data: dict):
    try:
        return StoryItem(**data)
    except ValidationError as e:
        raise ParseGraphError(e.errors()) from e


def parse_graph(story_item: StoryItem) -> tuple[DefaultDict[str, list], set]:
    """
    Function that represent users story like a graph.
    Second return value is a root node.
    """
    try:
        graph = defaultdict(list)
        exit_nodes = set()
        for key, options in story_item.nodes.items():
            for option in options.options:
                if option.next is None:
                    exit_nodes.add(key)
                    continue
                graph[option.next].append(key)
            if not options.options:
                exit_nodes.add(key)
        return graph, exit_nodes
    except KeyError as e:
        raise ParseGraphError(str(e)) from e
