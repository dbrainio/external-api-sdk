import asyncio

from typing import Optional, Dict, Any

from externalapi.utils.APIConnector import APIConnector


class Autocode(APIConnector):
    _gateway = 'https://b2b-api.checkperson.ru/b2b/api/v1'
    _report_name = 'report_individual_test@dbrain'

    def __init__(self, secret: str, gateway: Optional[str] = None, report_name: Optional[str] = None):
        self._gateway = self._gateway if gateway is None else gateway
        self._report_name = self._report_name if report_name is None else report_name
        self._secret = secret
        self._session_headers = {
            'Authorization': self._secret,
            'Content-Type': 'application/json'
        }

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
