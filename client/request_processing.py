import os

from entities.schemas import Node, Story, StoryList

API_URL = os.environ.get("API_URL", "http://localhost:5000/api")


class RequestManager:
    def __init__(self, session):
        self.session = session

    async def get_story_list(self):
        async with self.session.get(f"{API_URL}/story") as response:
            data = await response.json()
            return StoryList(**data)

    async def get_story(self, story_id):
        async with self.session.get(f"{API_URL}/story/{story_id}") as response:
            data = await response.json()
            return Story(**data)

    async def get_node(self, story_id, node_id):
        async with self.session.get(
            f"{API_URL}/story/{story_id}/nodes/{node_id}"
        ) as response:
            data = await response.json()
            return Node(**data)
