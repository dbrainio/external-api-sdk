import asyncio
from typing import Coroutine, Any


def run_sync(coro: Coroutine) -> Any:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coro)
    return result
