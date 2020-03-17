import asyncio
from functools import partial
from typing import Optional, Dict, Any

from externalapi.utils.APIConnector import APIConnector


class Autocode(APIConnector):
    _gateway = 'https://b2b-api.checkperson.ru/b2b/api/v1'

    def __init__(self, secret: str, report_name: str, gateway: Optional[str] = None):
        self._gateway = self._gateway if gateway is None else gateway
        self._report_name = report_name
        self._secret = secret
        self._session_headers = {
            'Authorization': self._secret,
            'Content-Type': 'application/json'
        }

    async def get_vehicle_info_by_vin(self, vin: str, auto_close_session: bool = False) -> Optional[dict]:
        return await self.get_vehicle_info('VIN', vin, auto_close_session)

    async def get_vehicle_info_by_grz(self, grz: str, auto_close_session: bool = False) -> Optional[dict]:
        return await self.get_vehicle_info('GRZ', grz, auto_close_session)

    async def get_vehicle_info_by_sts_number(self, sts: str, auto_close_session: bool = False) -> Optional[dict]:
        return await self.get_vehicle_info('STS', sts, auto_close_session)

    async def get_vehicle_info_by_pts_number(self, pts: str, auto_close_session: bool = False) -> Optional[dict]:
        return await self.get_vehicle_info('PTS', pts, auto_close_session)

    async def get_vehicle_info(self, key: str, query: str, auto_close_session: bool = False) -> Optional[dict]:
        """Get vehicle info"""
        session = self.session
        response = await self._make_report(key, query)
        if response['state'] == 'ok':
            report = await self._get_report(response['data'][0]['uid'])
        else:
            report = None
        if report is not None:
            data = self._parse_response(report)
        else:
            data = None
        if auto_close_session:
            await session.close()
            self._session = None
        return data

    async def _make_report(self, key: str, query: str) -> Dict[str, Any]:
        url = self._gateway + f'/user/reports/{self._report_name}/_make'
        payload = {
            'queryType': key,
            'query': query
        }
        data = await self._request(url, 'POST', payload)
        return data

    async def _get_report(self, report_id: str) -> Optional[dict]:
        url = self._gateway + f'/user/reports/{report_id}?_content=true&_detailed=true'
        retries = 10
        result = None
        while retries >= 0:
            data = await self._request(url, 'GET')
            if data['state'] == 'ok' and data['size'] > 0:
                if data['data'][0]['progress_wait'] != 0:
                    await asyncio.sleep(2)
                    retries -= 1
                else:
                    result = data['data'][0]['content']
                    break
            else:
                break
        return result

    @staticmethod
    def _parse_response(payload: dict) -> dict:
        _get = partial(Autocode._get_if_exists, payload)

        result = {}
        result['vin'] = _get(('identifiers', 'vehicle', 'vin'))
        result['reg_num'] = _get(('identifiers', 'vehicle', 'reg_num'))
        result['sts'] = _get(('identifiers', 'vehicle', 'sts'))
        result['pts'] = _get(('identifiers', 'vehicle', 'pts'))
        result['body'] = _get(('identifiers', 'vehicle', 'body'))
        result['chassis'] = _get(('identifiers', 'vehicle', 'chassis'))

        result['last_registered'] = {
            'region': _get(('registration_actions', 'items', -1, 'geo', 'region')),
            'city': _get(('registration_actions', 'items', -1, 'geo', 'city')),
            'owner': _get(('registration_actions', 'items', -1, 'owner', 'type')),
            'date_from': _get(('registration_actions', 'items', -1, 'date', 'start'))
        }

        result['year'] = _get(('tech_data', 'year'))
        result['weight'] = {
            'netto': _get(('tech_data', 'weight', 'netto')),
            'max': _get(('tech_data', 'weight', 'max'))
        }
        result['brand_model_rus'] = _get(('tech_data', 'brand', 'name', 'original'))
        result['type'] = _get(('tech_data', 'type', 'name'))
        result['brand'] = _get(('tech_data', 'brand', 'name', 'normalized'))
        result['model'] = _get(('tech_data', 'model', 'name', 'normalized'))
        result['color'] = _get(('tech_data', 'body', 'color', 'name'))
        result['drive'] = _get(('tech_data', 'drive', 'type'))

        result['engine'] = {
            'volume': _get(('tech_data', 'engine', 'volume')),
            'power': {
                'hp': _get(('tech_data', 'engine', 'power', 'hp')),
                'kw': _get(('tech_data', 'engine', 'power', 'kw'))
            },
            'fuel': _get(('tech_data', 'engine', 'fuel', 'type')),
            'model': _get(('tech_data', 'engine', 'model', 'name')),
            'number': _get(('tech_data', 'engine', 'number'))
        }

        result['category'] = _get(('additional_info', 'vehicle', 'category', 'code'))
        result['owner'] = {
            'region': _get(('additional_info', 'vehicle', 'owner', 'geo', 'region')),
            'city': _get(('additional_info', 'vehicle', 'owner', 'geo', 'city')),
            'postal_code': _get(('additional_info', 'vehicle', 'owner', 'geo', 'postal_code')),
        }
        return result
