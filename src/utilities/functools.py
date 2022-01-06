def parse_graph(data: dict):
    """Function that represent users story like a graph"""
    nodes = data["nodes"]
    graph = {}
    for key, options in nodes.items():
        graph[key] = [option["next"] for option in options["options"]]
    return graph
