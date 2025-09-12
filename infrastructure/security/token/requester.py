import requests

from typing import Tuple
from infrastructure.security.token.TOKEN_URLS import REMOTE_VALIDATE_TOKEN
from infrastructure.security.token.exception.verify_exception import \
    TokenRequestGetter
from settings import APP_ID


class TokenRequester:

    @staticmethod
    def _parse_response(result: requests.Response) -> Tuple[bool, dict]:
        r_json: dict = result.json()
        if not r_json.get('validate'):
            return False, r_json
        return r_json['validate'], r_json['payload']

    def request_for_validate(self, token) -> Tuple[bool, dict]:
        try:
            result = requests.post(
                url=REMOTE_VALIDATE_TOKEN, json={
                    f'token: {token}, app: {APP_ID}'}
            )
        except requests.exceptions.RequestException as e:
            raise TokenRequestGetter(detail=str(e), status_code=403)
        return self._parse_response(result)
