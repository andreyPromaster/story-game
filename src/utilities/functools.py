from pydantic import ValidationError

from common.entities.schemas import StoryItem
from utilities.exceptions import ParseGraphError


def parse_story_structure(data: dict):
    try:
        return StoryItem(**data)
    except ValidationError as e:
        raise ParseGraphError(e.errors()) from e


def parse_graph(story_item: StoryItem):
    """
    Function that represent users story like a graph.
    Second return value is a root node.
    """
    try:
        nodes = story_item.nodes
        graph = {}
        for key, options in nodes.items():
            graph[key] = [option.next for option in options.options]
        return graph, story_item.root
    except KeyError as e:
        raise ParseGraphError(str(e)) from e
