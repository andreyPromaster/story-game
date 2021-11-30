import abc


class DataDriver(abc.ABC):
    @abc.abstractmethod
    def get_story(self, story_id: str):
        """Get story from different source by story_id"""

    @abc.abstractmethod
    def get_node(self, story_id: str, uri: str):
        """Get story node from source by story_id and nodes URI"""

    @abc.abstractmethod
    def get_story_list(self):
        """Get list of stories"""
