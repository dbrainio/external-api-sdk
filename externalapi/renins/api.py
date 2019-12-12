import zeep

from externalapi.utils.APIConnector import APIConnectorException


from typing import Dict, Optional, List


class Renins:
    def __init__(self, wsdl_url: str, login: str, password: str):
        self._client = zeep.Client(wsdl=wsdl_url)

        self._credentials = {
            'Login': login,
            'Password': password
        }

    def request(self, claim_type: str, catalog_code: str) -> List[Dict[str, Optional[str]]]:
        payload = {
            **self._credentials,
            'ClaimType': claim_type,
            'CatalogCode': catalog_code
        }
        response = self._client.service.process(payload)
        if response.Payload is None:
            if response.Message:
                raise APIConnectorException(-1, response.Message.ErrorMessage)
            else:
                result = []
        else:
            result = zeep.helpers.serialize_object(
                response.Payload._value_1[0]['Catalog'].CatalogEntry,
                target_cls=dict
            )
        return result
