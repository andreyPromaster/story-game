import asyncio

import aiohttp
from request_processing import RequestManager


async def show_stories(request_manager):
    data = await request_manager.get_story_list()
    print("Available stories:")
    for number, story in enumerate(data.stories, 1):
        print(f"{number}. {story.id}")


async def start_game():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        request_manager = RequestManager(session=session)
        await show_stories(request_manager)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_game())
