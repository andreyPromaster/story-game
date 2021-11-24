from data_storage.data_source import DataDriver


class RDSDriver(DataDriver):
    def get_story(self, story_id: str):
        raise NotImplementedError

    def get_node(self, story_id: str, uri: str):
        raise NotImplementedError

    def get_story_list(self):
        raise NotImplementedError
