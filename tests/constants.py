VALID_STORY_ITEM = (
    (
        {
            "Root": ["Node1"],
            "Node1": ["Root"],
        },
        {"Root"},
    ),
    (
        {
            "Root": ["Node1"],
            "Node1": ["Root"],
        },
        {"Node1"},
    ),
    (
        {
            "Node1": [],
            "Node2": ["Node1"],
            "Node3": ["Node2", "Node1"],
            "Node4": ["Node1", "Node3"],
        },
        {"Node2", "Node4"},
    ),
    (
        {
            "Node1": ["Node2"],
            "Node2": ["Node1", "Node6"],
            "Node3": ["Node1"],
            "Node4": ["Node2", "Node3"],
            "Node5": ["Node3"],
            "Node6": ["Node4"],
        },
        {"Node5"},
    ),
)


CYCLE_STORY_GRAPHS = (
    (
        {
            "Root": [],
            "Node1": ["Root", "Node2"],
            "Node2": ["Node1"],
        },
        {},
    ),
    (
        {
            "Node1": ["Node2"],
            "Node2": ["Node1"],
            "Node3": ["Node1", "Node5"],
            "Node4": ["Node3", "Node2", "Node6"],
            "Node5": ["Node3"],
            "Node6": ["Node4"],
        },
        {"Node5"},
    ),
    (
        {
            "Node1": [],
            "Node2": ["Node1"],
            "Node3": ["Node1", "Node5", "Node4"],
            "Node4": ["Node5", "Node3"],
            "Node5": ["Node3", "Node4"],
            "Node6": ["Node2"],
        },
        {"Node6"},
    ),
)
