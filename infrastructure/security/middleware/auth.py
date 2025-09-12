import time
from functools import lru_cache

import cachetools
from fastapi import Request
from starlette.authentication import AuthenticationBackend

from domain.auth.service import AuthService
from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User
from infrastructure.security.middleware.exception.auth_exception import \
    TokenAuthException
from infrastructure.security.token.requester import TokenRequester


class TokenAuthBackend(AuthenticationBackend):

    @cachetools.cached(
        cache=cachetools.TTLCache(
            maxsize=128,
            ttl=10 * 60
        )
    )
    def _get_user(self, user_identifier) -> User:
        up_db = UserPermissionDBAPI()
        ats = AuthService(up_db)
        return ats.get_user_with_permission(user_identifier)

    async def authenticate(self, request: Request):
        try:
            token = request.headers["Authorization"]
        except KeyError as exc:
            ui = request.cookies.get('user_identifier')
            if ui:
                return None, User(hash_identifier=ui)
            else:
                raise TokenAuthException(
                    detail='Not authorize',
                    status_code=400
                )

        tr = TokenRequester()
        validate, payload = tr.request_for_validate(token)

        if not validate:
            raise TokenAuthException(
                detail='Invalid JWT Token.',
                status_code=400
            )
        user = self._get_user(payload['user_identifier'])
        return None, user