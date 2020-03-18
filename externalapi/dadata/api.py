from datetime import datetime

from externalapi.utils.APIConnector import APIConnector

from typing import Optional, Dict, Any, Union, List


class Dadata(APIConnector):
    _suggest_gateway = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/{method}/{resource}'
    _cleaner_gateway = 'https://cleaner.dadata.ru/api/v1/clean/{resource}'

    def __init__(self,
                 apikey: str, secret: Optional[str] = None,
                 suggest_gateway: Optional[str] = None, cleaner_gateway: Optional[str] = None):
        self._suggest_gateway = self._suggest_gateway if suggest_gateway is None else suggest_gateway
        self._cleaner_gateway = self._cleaner_gateway if cleaner_gateway is None else cleaner_gateway
        self._api_key = apikey
        self._secret = secret

        headers = {
            'Authorization': f'Token {self._api_key}',
            'Content-Type': 'application/json'
        }
        if self._secret:
            headers['X-Secret'] = self._secret
        self._session_headers = headers

    async def _get_suggest(self,
                           method: Union['suggest', 'findById'],
                           resource: Union['address', 'email', 'fms_unit', 'fio'],
                           query: Union[str, dict]) -> List[Dict[str, Any]]:
        """Get Dadata suggests."""
        if method == 'findById' and resource != 'fms_unit':
            raise ValueError('findById works only for fms_unit')

        url = self._suggest_gateway.format(method=method, resource=resource)
        data = query if isinstance(query, dict) and 'query' in query.keys() else {'query': query}
        result = await self._request(url, 'POST', data)
        return result['suggestions']

    async def _get_cleaned(self,
                           resource: Union['phone', 'address', 'passport', 'name', 'email', 'birthdate', 'vehicle'],
                           query: List[str]) -> List[Dict[str, Any]]:
        """Get Dadata cleaned data."""
        url = self._cleaner_gateway.format(resource=resource)
        result = await self._request(url, 'POST', query)
        return result

    async def suggest_address(self, query: str) -> List[Dict[str, Any]]:
        """Get Dadata suggest on address."""
        result = await self._get_suggest('suggest', 'address', query)
        return result

    async def suggest_email(self, query: str) -> List[Dict[str, Any]]:
        """Get Dadata suggest on email."""
        result = await self._get_suggest('suggest', 'email', query)
        return result

    async def suggest_fms_unit(self, query: str) -> List[Dict[str, Any]]:
        """Get Dadata suggest on fms_unit."""
        result = await self._get_suggest('suggest', 'fms_unit', query)
        return result

    async def suggest_organisation(self, query: str, orgtype: Union['INDIVIDUAL', 'LEGAL']) -> Dict[str, Any]:
        """Get Dadata suggest on organisation."""
        if orgtype not in ('INDIVIDUAL', 'LEGAL'):
            raise ValueError(f'Incorrect ogrtype. Expected INDIVIDUAL/LEGAL, fot {orgtype}')

        query = {
            'query': query,
            'type': orgtype
        }
        result = await self._get_suggest('suggest', 'party', query)
        processed = self._process_org(result, orgtype == 'LEGAL')
        return processed

    def _process_org(self, suggestions: List[Dict[str, Any]], is_legal: bool = True) -> Dict[str, Any]:
        result = {
            'name': {
                'short': '',
                'full': ''
            },
            'number': '',
            'date_of_registration': '',
            'director_name': '',
            'director_post': '',
            'address': '',
            'inn': '',
            'kpp': ''
        }

        if not suggestions:
            return result
        data = suggestions[0]['data']

        result['name']['full'] = self._get_if_exists(data, ('name', 'full_with_opf'))
        ts = self._get_if_exists(data, ('state', 'registration_date'))
        if ts:
            ts = int(ts / 1000)
            result['date_of_registration'] = datetime.utcfromtimestamp(ts).strftime('%d.%m.%Y')
        result['inn'] = self._get_if_exists(data, ('inn', ))
        result['number'] = self._get_if_exists(data, ('ogrn', ))

        if is_legal:
            result['name']['short'] = self._get_if_exists(data, ('name', 'short'))
            result['director_name'] = self._get_if_exists(data, ('management', 'name'))
            result['director_post'] = self._get_if_exists(data, ('management', 'post'))
            result['address'] = self._get_if_exists(data, ('address', 'unrestricted_value'))
            result['kpp'] = self._get_if_exists(data, ('kpp', ))

        return result

    async def suggest_fio(self, query: str) -> List[Dict[str, Any]]:
        """Get Dadata suggest on fio."""
        result = await self._get_suggest('suggest', 'fio', query)
        return result

    async def find_fms_unit_by_code(self, query: str) -> List[Dict[str, Any]]:
        """Get Dadata suggests for fms_unit by unit code."""
        result = await self._get_suggest('findById', 'fms_unit', query)
        return result

    async def clean_address(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of addresses using Dadata standartize API."""
        result = await self._get_cleaned('address', query)
        return result

    async def clean_email(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of emails using Dadata standartize API."""
        result = await self._get_cleaned('email', query)
        return result

    async def clean_phone(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of phones using Dadata standartize API."""
        result = await self._get_cleaned('phone', query)
        return result

    async def clean_vehicle(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of vehicles using Dadata standartize API."""
        result = await self._get_cleaned('vehicle', query)
        return result

    async def clean_passport(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of passports using Dadata standartize API."""
        result = await self._get_cleaned('passport', query)
        return result

    async def clean_fio(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of fio using Dadata standartize API."""
        result = await self._get_cleaned('name', query)
        return result

    async def clean_date(self, query: List[str]) -> List[Dict[str, Any]]:
        """Clean a list of dates using Dadata standartize API."""
        result = await self._get_cleaned('birthdate', query)
        return result
