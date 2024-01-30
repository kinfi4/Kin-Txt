from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from kin_statistics_api.domain.entities import UserLoginEntity, UserRegistrationEntity, User
from kin_statistics_api.exceptions import LoginFailedError, UsernameAlreadyTakenError
from kin_statistics_api.domain.services import UserService
from kin_statistics_api.containers import Container
from kin_statistics_api.views.helpers.auth import get_current_user

router = APIRouter(prefix="/accounts")


@router.post("/login")
@inject
def login(
    user_data: UserLoginEntity,
    user_service: UserService = Depends(Provide[Container.services.user_service]),
):
    try:
        token = user_service.login(user_data)
    except LoginFailedError:
        return JSONResponse(
            content={'errors': 'Username and/or password are incorrect'},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={'token': token})


@router.post("/register")
@inject
async def register(
    user_data: UserRegistrationEntity,
    user_service: UserService = Depends(Provide[Container.services.user_service]),
):
    try:
        token = user_service.register(user_data)
    except UsernameAlreadyTakenError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'errors': 'User with specified username already exists'}
        )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'token': token})


@router.get("/me")
async def get_current_user(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"username": current_user.username})
