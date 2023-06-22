from fastapi import Header, HTTPException, status, Request

from kin_news_core.auth import decode_jwt_token, decode_kin_token
from kin_news_core.constants import KIN_TOKEN_PREFIX
from kin_news_core.exceptions import AuthenticationFailedError
from kin_statistics_api.domain.entities import User
from kin_statistics_api.settings import Settings


INTERNAL_URLS = [
    "/api/v1/reports-data/save",
]


def get_current_user(request: Request, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if authorization.startswith(KIN_TOKEN_PREFIX) and request.url.path in INTERNAL_URLS:
        try:
            decoded_token = decode_kin_token(authorization)
        except AuthenticationFailedError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        if decoded_token != Settings().kin_token:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        return User(username="", internal_user=True)

    try:
        decoded_username = decode_jwt_token(authorization)
    except AuthenticationFailedError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return User(username=decoded_username)
