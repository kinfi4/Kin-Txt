from fastapi import Header, HTTPException, status, Request

from kin_news_api.domain.entities import UserEntity
from kin_news_core.auth import decode_jwt_token
from kin_news_core.exceptions import AuthenticationFailedError


AUTH_LESS_URLS = [
    "/api/v1/accounts/login",
    "/api/v1/accounts/register",
]


def get_current_user(request: Request, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        decoded_username = decode_jwt_token(authorization)
    except AuthenticationFailedError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return UserEntity(username=decoded_username)
