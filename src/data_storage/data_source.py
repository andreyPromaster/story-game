import abc

from common.entities.schemas import Node, Story, StoryList
from data_storage.validators import (
    is_existing_graph_cycle,
    is_existing_root_node,
    is_existing_unconnected_node,
    is_existing_unrelated_reference,
)


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
        self._validate_story_item(data)
        self._create_story(data)

    @abc.abstractmethod
    def _create_story(self, data):
        raise NotImplementedError

    @staticmethod
    def _validate_story_item(story_data):
        is_existing_root_node(story_data)
        is_existing_unconnected_node(story_data)
        is_existing_unrelated_reference(story_data)
        is_existing_graph_cycle(story_data)
