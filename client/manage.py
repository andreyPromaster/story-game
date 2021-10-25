import asyncio
from typing import List

import aiohttp
from aiohttp import ClientResponseError
from exception import ExitException
from request_processing import RequestManager

from entities.schemas import Node


def get_user_input():
    while True:
        try:
            user_input = input("Enter record number: ")
            if str(user_input) == "exit":
                raise ExitException
            user_choice = int(user_input)
            return user_choice - 1
        except ValueError:
            print("Try again, invalid input")


def get_list_row(data: List):
    while True:
        choice = get_user_input()
        if choice >= 0:
            try:
                row = data[choice]
                return row
            except IndexError:
                print("Input out of data range!")
        else:
            print("Input out of data range!")


def show_stories(stories):
    print("Available stories:")
    if stories:
        for number, story in enumerate(stories, 1):
            print(f"{number}. {story.id}")
    else:
        print("Can't find any stories(")


async def manage_stories(request_manager):
    data = await request_manager.get_story_list()
    show_stories(data.stories)
    return get_list_row(data.stories)


def show_story_node(node: Node):
    print(f"INFO: {node.text}")
    for num, option in enumerate(node.options, 1):
        print(f"{num}. {option.text}")


async def manage_story_node(request_manager, story_id, node_id):
    try:
        data = await request_manager.get_node(story_id=story_id, node_id=node_id)
    except ClientResponseError:
        return None
    show_story_node(data)
    return get_list_row(data.options)


async def start_game():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        try:
            request_manager = RequestManager(session=session)
            selected_story = await manage_stories(request_manager)
            print("____Story starts____")
            next_node = selected_story.root
            while True:
                node = await manage_story_node(
                    request_manager, selected_story.id, next_node
                )
                next_node = node
                if node is None:
                    print("Story has ended!")
                    break
        except ExitException:
            print("Goodbuy")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_game())
