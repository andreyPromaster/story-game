import abc

from common.entities.schemas import Node, Story, StoryList
from data_storage.validators import (
    is_existing_graph_cycle,
    is_existing_root_node,
    is_existing_unconnected_node,
    is_existing_unrelated_reference,
)
from utilities.functools import parse_graph, parse_story_structure


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

    def create_story(self, data: dict):
        """
        Template method.
        Raise exception if unsuccessful.
        Validate and create story item
        """
        validated_story_data = parse_story_structure(data)
        self.validate_story_item(validated_story_data)
        self._create_story(validated_story_data)
        return validated_story_data

    @abc.abstractmethod
    def _create_story(self, data):
        """
        Method, that responds for creation of a history for a specific driver.
        """

    @staticmethod
    def validate_story_item(validated_story_data):
        graph, exit_nodes = parse_graph(validated_story_data)
        root_node = validated_story_data.root
        is_existing_root_node(validated_story_data)
        is_existing_unconnected_node(graph, root_node, exit_nodes)
        is_existing_unrelated_reference(graph)
        is_existing_graph_cycle(graph, exit_nodes)
