from fastapi import Header, HTTPException, status, Request

from kin_txt_core.auth import decode_jwt_token
from kin_txt_core.exceptions import AuthenticationFailedError

from kin_generic_builder.api.entities import User

INTERNAL_URLS: list[str] = []


def get_current_user(request: Request, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        decoded_username = decode_jwt_token(authorization)
    except AuthenticationFailedError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return User(username=decoded_username)
