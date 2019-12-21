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
            res = cur_val.get(key)
            if res:
                cur_val = res
        return res

    async def get_vehicle_info(self, vin: str, auto_close_session: bool = True) -> Optional[dict]:
        """Get vehicle info by VIN."""
        session = self.session
        response = await self._make_report(vin)
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

    async def _make_report(self, vin: str) -> Dict[str, Any]:
        url = self._gateway + f'/user/reports/{self._report_name}/_make'
        payload = {
            'queryType': 'VIN',
            'query': vin
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
        identifiers = payload.get('identifiers')
        if identifiers:
            vehicle = identifiers.get('vehicle')
            if vehicle:
                result['vin'] = vehicle.get('vin')
                result['reg_num'] = vehicle.get('reg_num')
                result['sts'] = vehicle.get('sts')
                result['pts'] = vehicle.get('pts')

        reg_acts = payload.get('registration_actions')
        if reg_acts:
            last_reg = reg_acts['items'][-1]
            result['last_registered'] = {
                'region': Autocode._get_if_exists(last_reg, ('geo', 'region')),
                'city': Autocode._get_if_exists(last_reg, ('geo', 'city')),
                'owner': Autocode._get_if_exists(last_reg, ('owner', 'type')),
                'date_from': Autocode._get_if_exists(last_reg, ('date', 'start'))
            }

        tech_data = payload.get('tech_data')
        if tech_data:

            result['year'] = tech_data.get('year')
            result['weight'] = {
                'netto': Autocode._get_if_exists(tech_data, ('weight', 'netto')),
                'max': Autocode._get_if_exists(tech_data, ('weight', 'max'))
            }
            result['brand_model_rus'] = Autocode._get_if_exists(tech_data, ('brand', 'name', 'original'))
            result['type'] = Autocode._get_if_exists(tech_data, ('type', 'name'))
            result['brand'] = Autocode._get_if_exists(tech_data, ('brand', 'name', 'normalized'))
            result['model'] = Autocode._get_if_exists(tech_data, ('model', 'name', 'normalized'))
            result['color'] = Autocode._get_if_exists(tech_data, ('body', 'color', 'name'))

        engine = tech_data.get('engine')
        if engine:
            result['engine'] = {
                'volume': engine.get('volume'),
                'power': {
                    'hp': Autocode._get_if_exists(engine, ('power', 'hp')),
                    'kw': Autocode._get_if_exists(engine, ('power', 'kw'))
                },
                'fuel': Autocode._get_if_exists(engine, ('fuel', 'type')),
                'model': Autocode._get_if_exists(engine, ('model', 'name'))
            }
        if payload.get('additional_info'):
            result['category'] = Autocode._get_if_exists(payload, ('additional_info', 'vehicle', 'category', 'code'))
        return result
