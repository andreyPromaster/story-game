from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List

from pydantic import ValidationError

from common.entities.schemas import StoryItem
from utilities.exceptions import ParseGraphError


def parse_story_structure(data: dict):
    try:
        return StoryItem(**data)
    except ValidationError as e:
        raise ParseGraphError(e.errors()) from e


def parse_graph_as_incidence_matrix(story_item: StoryItem) -> Dict[str, List]:
    """
    Key is node name, list contains nodes references to others node
    """
    try:
        nodes = story_item.nodes
        graph = {}
        for key, options in nodes.items():
            graph[key] = [option.next for option in options.options]
        return graph
    except KeyError as e:
        raise ParseGraphError(str(e)) from e


def parse_graph(story_item: StoryItem) -> tuple[DefaultDict[str, list], set]:
    """
    Function that represent users story like a graph.
    Key is node name, list contains references to this node.
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
