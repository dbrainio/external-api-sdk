import json
from pathlib import Path

from aiohttp import ClientSession, TCPConnector

from typing import Optional, List, Dict, Any

__config_path = Path(__file__).absolute().parent.parent / 'configs' / 'dadata.json'
__config = json.load(__config_path.open())


async def _get_suggest(method: str, resource: str, query: str) -> Dict[List[Dict[str, Any]]]:
    url = __config['gateway']['suggest'].format(method=method, resource=resource)
    async with ClientSession(
            headers={'Authorization': __config['token'], 'Content-Type': 'application/json'},
            connector=TCPConnector(verify_ssl=False)) as session:
        async with session.post(url, data=json.dumps({'query': query})) as response:
            data = await response.json()

    return data


async def _get_cleaned():
    raise NotImplementedError('Need to get SCRET KEY')


async def get_address_suggest(query: str) -> Optional[List[Dict[str, Any]]]:
    result = _get_suggest('suggest', 'address', query)
    return result['suggestions'] if result else None


async def get_fio_suggest(query: str) -> Optional[List[Dict[str, Any]]]:
    result = _get_suggest('suggest', 'fio', query)
    return result['suggestions'] if result else None


async def get_fms_suggest(query: str) -> Optional[List[Dict[str, Any]]]:
    result = _get_suggest('suggest', 'fms_unit', query)
    return result['suggestions'] if result else None


async def get_fms_suggest_by_code(query: str) -> Optional[List[Dict[str, Any]]]:
    result = _get_suggest('findById', 'fms_unit', query)
    return result['suggestions'] if result else None
