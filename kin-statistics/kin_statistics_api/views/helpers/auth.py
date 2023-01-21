from fastapi import Header, HTTPException, status

from kin_statistics_api.domain.entities import User


def get_current_user(authentication: str = Header(...)):
    if not authentication:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    print(f"AUTHENTICATION HEADER: {authentication}")

    return User(username="kinfi4")
