from typing import Dict, TypedDict


class StoryItem(TypedDict):
    graph: Dict[str, list]
    exit_nodes: set


VALID_STORY_ITEM = (
    StoryItem(
        graph={
            "Root": ["Node1"],
            "Node1": ["Root"],
        },
        exit_nodes={"Root"},
    ),
    StoryItem(
        graph={
            "Root": ["Node1"],
            "Node1": ["Root"],
        },
        exit_nodes={"Node1"},
    ),
    StoryItem(
        graph={
            "Node1": [],
            "Node2": ["Node1"],
            "Node3": ["Node2", "Node1"],
            "Node4": ["Node1", "Node3"],
        },
        exit_nodes={"Node2", "Node4"},
    ),
    StoryItem(
        graph={
            "Node1": ["Node2"],
            "Node2": ["Node1", "Node6"],
            "Node3": ["Node1"],
            "Node4": ["Node2", "Node3"],
            "Node5": ["Node3"],
            "Node6": ["Node4"],
        },
        exit_nodes={"Node5"},
    ),
)

CYCLE_STORY_GRAPHS = (
    StoryItem(
        graph={
            "Root": [],
            "Node1": ["Root", "Node2"],
            "Node2": ["Node1"],
        },
        exit_nodes=set(),
    ),
    StoryItem(
        graph={
            "Node1": ["Node2"],
            "Node2": ["Node1"],
            "Node3": ["Node1", "Node5"],
            "Node4": ["Node3", "Node2", "Node6"],
            "Node5": ["Node3"],
            "Node6": ["Node4"],
        },
        exit_nodes={"Node5"},
    ),
    StoryItem(
        graph={
            "Node1": [],
            "Node2": ["Node1"],
            "Node3": ["Node1", "Node5", "Node4"],
            "Node4": ["Node5", "Node3"],
            "Node5": ["Node3", "Node4"],
            "Node6": ["Node2"],
        },
        exit_nodes={"Node6"},
    ),
)
PARSED_STORY_GRAPH = (
    (
        "tests/unit/test_json/valid_story.json",
        {
            "Root": ["Node2"],
            "Node1": ["Root"],
            "Node2": ["Node1"],
        },
        {"Root", "Node1", "Node2"},
    ),
    (
        "tests/unit/test_json/story_item_with_unrelated_references.json",
        {
            "Node1": ["Root"],
            "Node2": ["Root"],
            "Node3": ["Root"],
        },
        set(),
    ),
    (
        "tests/unit/test_json/story_item_without_node_options.json",
        {"Node1": ["Root"], "Node2": ["Root"]},
        {"Node1", "Node2"},
    ),
    (
        "tests/unit/test_json/story_item_changed_default_root_node.json",
        {"Node2": ["Node1"]},
        {"Node1", "Node2"},
    ),
)
PARSED_STORY_GRAPH_AS_INCIDENCE_MATRIX = (
    (
        "tests/unit/test_json/valid_story.json",
        {
            "Root": ["Node1", None],
            "Node1": ["Node2", None],
            "Node2": [None, "Root"],
        },
    ),
    (
        "tests/unit/test_json/story_item_with_unrelated_references.json",
        {
            "Root": ["Node1", "Node2", "Node3"],
        },
    ),
    (
        "tests/unit/test_json/story_item_without_node_options.json",
        {
            "Root": ["Node1", "Node2"],
            "Node1": [],
            "Node2": [],
        },
    ),
    (
        "tests/unit/test_json/story_item_changed_default_root_node.json",
        {
            "Node1": ["Node2", None],
            "Node2": [None, None],
        },
    ),
    (
        "tests/unit/test_json/story_item_with_group_unconnected_nodes.json",
        {
            "Root": [None, "Root1"],
            "Root1": [None, None],
            "Node1": ["Node2"],
            "Node2": ["Node3"],
            "Node3": ["Node1", None],
        },
    ),
)
