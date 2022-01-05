import abc

from common.entities.schemas import Node, Story, StoryList


class DataDriver(abc.ABC):
    @abc.abstractmethod
    def get_story(self, story_id: str) -> Story:
        """Get story from different source by story_id"""

    @abc.abstractmethod
    def get_node(self, story_id: str, uri: str) -> Node:
        """Get story node from source by story_id and nodes URI"""

    @abc.abstractmethod
    def get_story_list(self) -> StoryList:
        """Get list of stories"""

    @abc.abstractmethod
    def create_story(self, data: dict):
        """
        Template method.
        Raise exception if unsuccessful.
        Validate and create story item
        """
        self._validate_story_item(data)
        self._create_story(data)

    @abc.abstractmethod
    def _create_story(self, data):
        raise NotImplementedError

    def _validate_story_item(self, story_data):
        pass

    def parse_graph(self, data: dict):
        """Move to other file"""
        nodes = data["nodes"]
        graph = {}
        for key, options in nodes.items():
            graph[key] = [option["next"] for option in options]
        return graph
