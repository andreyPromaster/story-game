from common.entities.schemas import StoryItem


def parse_graph(data: dict):
    """
    Function that represent users story like a graph.
    Second return value is a root node.
    """
    story_item = StoryItem(**data)

    nodes = story_item.nodes
    graph = {}
    for key, options in nodes.items():
        graph[key] = [option.next for option in options.options]
    return graph, story_item.root
