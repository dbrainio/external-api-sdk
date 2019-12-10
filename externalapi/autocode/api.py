import json
import asyncio
from pathlib import Path

from aiohttp import ClientSession, TCPConnector

from typing import Optional

__config_path = Path(__file__).absolute().parent.parent.parent / 'configs' / 'autocode.json'
__config = json.load(__config_path.open())


async def _get_report(session: ClientSession, report_id: str) -> Optional[dict]:
    url = __config['gateway'] + f'/user/reports/{report_id}?_content=true&_detailed=true'
    async with session.get(url) as response:
        data = await response.json()

    if data['state'] == 'ok' and data['size'] > 0:
        if data['data'][0]['progress_wait'] != 0:
            await asyncio.sleep(0.1)
            result = await _get_report(session, report_id)
        else:
            result = data['data'][0]['content']
    else:
        result = None
    return result


async def _make_report(session: ClientSession, vin: str) -> str:
    url = __config['gateway'] + '/user/reports/{}/_make'.format(__config['report'])
    payload = {
        'queryType': 'VIN',
        'query': vin
    }
    async with session.post(url, data=json.dumps(payload)) as response:
        data = await response.json()
    return data


def _parse_response(payload: dict) -> dict:
    result = {}
    identifiers = payload.get('identifiers')
    if identifiers:
        result['vin'] = identifiers['vehicle']['vin']
        result['reg_num'] = identifiers['vehicle']['reg_num']
        result['sts'] = identifiers['vehicle']['sts']
        result['pts'] = identifiers['vehicle']['pts']

    reg_acts = payload.get('registration_actions')
    if reg_acts:
        last_reg = reg_acts['items'][-1]
        result['last_registered'] = {
            'region': last_reg['geo']['region'],
            'city': last_reg['geo']['city'],
            'owner': last_reg['owner']['type'],
            'date_from': last_reg['date']['start']
        }

    tech_data = payload.get('tech_data')
    if tech_data:
        result['brand'] = tech_data['brand']['name']['normalized']
        result['model'] = tech_data['model']['name']['normalized']
        result['year'] = tech_data['year']
        result['color'] = tech_data['body']['color']['name']
        result['weight'] = tech_data['weight']

    engine = tech_data.get('engine')
    if engine:
        result['engine'] = {
            'fuel': engine['fuel']['type'],
            'volume': engine['volume'],
            'power': engine['power'],
            'model': engine['model']['name']
        }
    if payload.get('additional_info'):
        result['category'] = payload['additional_info']['vehicle']['category']['code']
    return result


async def get_vehicle_info(vin: str):
    """Get vehicle info by VIN."""
    async with ClientSession(
            headers={'Authorization': __config['token'], 'Content-Type': 'application/json'},
            connector=TCPConnector(verify_ssl=False)) as session:
        response = await _make_report(session, vin)
        if response['state'] == 'ok':
            report = await _get_report(session, response['data'][0]['uid'])
        else:
            raise ValueError(response['event']['name'])
    if report is not None:
        data = _parse_response(report)
    else:
        data = None
    return data


def get_vehicle_info_sync(vin: str):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(get_vehicle_info(vin))
    loop.run_until_complete(task)
    result = task.result()
    return result
