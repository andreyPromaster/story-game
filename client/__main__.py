import asyncio

from .manage import start_game

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_game())
