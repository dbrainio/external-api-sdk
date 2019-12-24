import asyncio

from typing import Optional, Dict, Any, Iterable

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

    @staticmethod
    def _get_if_exists(data: dict, keys_chain: Iterable[str]) -> Optional[Any]:
        cur_val = data
        for key in keys_chain:
            if isinstance(cur_val, list):
                try:
                    res = cur_val[key]
                except IndexError:
                    res = ''
            else:
                res = cur_val.get(key, '')
            cur_val = res if res else {}
        return res

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
        data = await self._request(url, 'GET')

        if data['state'] == 'ok' and data['size'] > 0:
            if data['data'][0]['progress_wait'] != 0:
                await asyncio.sleep(0.1)
                result = await self._get_report(report_id)
            else:
                result = data['data'][0]['content']
        else:
            result = None
        return result

    @staticmethod
    def _parse_response(payload: dict) -> dict:
        result = {}
        result['vin'] = Autocode._get_if_exists(payload, ('identifiers', 'vehicle', 'vin'))
        result['reg_num'] = Autocode._get_if_exists(payload, ('identifiers', 'vehicle', 'reg_num'))
        result['sts'] = Autocode._get_if_exists(payload, ('identifiers', 'vehicle', 'sts'))
        result['pts'] = Autocode._get_if_exists(payload, ('identifiers', 'vehicle', 'pts'))

        result['last_registered'] = {
            'region': Autocode._get_if_exists(payload, ('registration_actions', 'items', -1, 'geo', 'region')),
            'city': Autocode._get_if_exists(payload, ('registration_actions', 'items', -1, 'geo', 'city')),
            'owner': Autocode._get_if_exists(payload, ('registration_actions', 'items', -1, 'owner', 'type')),
            'date_from': Autocode._get_if_exists(payload, ('registration_actions', 'items', -1, 'date', 'start'))
        }

        result['year'] = Autocode._get_if_exists(payload, ('tech_data', 'year'))
        result['weight'] = {
            'netto': Autocode._get_if_exists(payload, ('tech_data', 'weight', 'netto')),
            'max': Autocode._get_if_exists(payload, ('tech_data', 'weight', 'max'))
        }
        result['brand_model_rus'] = Autocode._get_if_exists(payload, ('tech_data', 'brand', 'name', 'original'))
        result['type'] = Autocode._get_if_exists(payload, ('tech_data', 'type', 'name'))
        result['brand'] = Autocode._get_if_exists(payload, ('tech_data', 'brand', 'name', 'normalized'))
        result['model'] = Autocode._get_if_exists(payload, ('tech_data', 'model', 'name', 'normalized'))
        result['color'] = Autocode._get_if_exists(payload, ('tech_data', 'body', 'color', 'name'))

        result['engine'] = {
            'volume': Autocode._get_if_exists(payload, ('tech_data', 'engine', 'volume')),
            'power': {
                'hp': Autocode._get_if_exists(payload, ('tech_data', 'engine', 'power', 'hp')),
                'kw': Autocode._get_if_exists(payload, ('tech_data', 'engine', 'power', 'kw'))
            },
            'fuel': Autocode._get_if_exists(payload, ('tech_data', 'engine', 'fuel', 'type')),
            'model': Autocode._get_if_exists(payload, ('tech_data', 'engine', 'model', 'name'))
        }

        result['category'] = Autocode._get_if_exists(payload, ('additional_info', 'vehicle', 'category', 'code'))

        return result
