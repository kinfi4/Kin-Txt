from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.entities import UserEntity, UserRegistrationEntity
from api.domain.services import UserService
from api.exceptions import LoginFailedError, UsernameAlreadyTakenError
from config.containers import Container
from kin_news_core.auth import JWTAuthentication
from kin_news_core.utils import pydantic_errors_prettifier


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.domain_services.user_service],
    ) -> Response:
        try:
            user_entity = UserEntity(**request.data)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})

        try:
            token = user_service.login(user_entity)
        except LoginFailedError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'errors': 'Username and/or password are incorrect'}
            )

        return Response(status=status.HTTP_200_OK, data={'token': token})


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.domain_services.user_service],
    ) -> Response:
        try:
            user_entity = UserRegistrationEntity(**request.data)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})

        try:
            token = user_service.register(user_entity)
        except UsernameAlreadyTakenError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': 'User with specified username already exists'}
            )

        return Response(status=status.HTTP_201_CREATED, data={'token': token})


class UserView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK, data={
            "username": request.user.username,
        })
