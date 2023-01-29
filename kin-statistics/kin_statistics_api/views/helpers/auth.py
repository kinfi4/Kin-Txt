from fastapi import Header, HTTPException, status

from kin_news_core.auth import decode_jwt_token
from kin_statistics_api.domain.entities import User


def get_current_user(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    decoded_username = decode_jwt_token(authorization)
    return User(username=decoded_username)
