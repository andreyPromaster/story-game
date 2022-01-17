from pydantic import ValidationError

from common.entities.schemas import StoryItem
from utilities.exceptions import ParseGraphError


def parse_graph(data: dict):
    """
    Function that represent users story like a graph.
    Second return value is a root node.
    """
    try:
        story_item = StoryItem(**data)

        nodes = story_item.nodes
        graph = {}
        for key, options in nodes.items():
            graph[key] = [option.next for option in options.options]
        return graph, story_item, story_item.root
    except ValidationError as e:
        raise ParseGraphError(e.errors()) from e
