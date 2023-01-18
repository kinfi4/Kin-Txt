from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.entities import CreateUserEntity
from api.domain.services import UserService
from api.exceptions import UsernameTaken
from config.containers import Container
from kin_news_core.auth.kin_token import KinTokenAuthentication


class RegisterUserView(APIView):
    authentication_classes = [KinTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.services.user_service],
    ) -> Response:
        try:
            create_user_entity = CreateUserEntity(username=request.data.get('username'))
            user_service.register_user(create_user_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})
        except UsernameTaken:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED, data={'message': 'OK'})
