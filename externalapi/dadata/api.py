import json
import asyncio
from pathlib import Path

from aiohttp import ClientSession, TCPConnector

from typing import Optional

__config_path = Path(__file__).absolute().parent.parent.parent / 'configs' / 'dadata.json'
__config = json.load(__config_path.open())


async def get_suggest():
    pass
