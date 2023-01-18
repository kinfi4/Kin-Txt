from dependency_injector.wiring import Provide, inject
from django.conf import settings
from pydantic import ValidationError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.entities import ChannelPostEntity
from api.domain.services import ChannelService
from api.exceptions import UserIsNotSubscribed, UserMaxSubscriptionsExceeded
from config.containers import Container
from kin_news_core.auth import JWTAuthentication
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.utils import pydantic_errors_prettifier


class ChannelListView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        channels = channel_service.get_user_channels(request.user)
        channels_serialized = [channel.dict(by_alias=True) for channel in channels]

        return Response(data=channels_serialized)

    @inject
    def post(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(**request.data)
            channel = channel_service.subscribe_user(request.user, channels_entity)
        except UserMaxSubscriptionsExceeded:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': f'We are sorry, but you have exceeded maximum number of subscriptions. '
                                f'You may subscribe only up to {settings.MAX_USER_SUBSCRIPTIONS} at the same time.'}
            )
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})
        except InvalidChannelURLError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(data=channel.dict(by_alias=True))


class ChannelUnsubscribeView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    @inject
    def delete(
        self,
        request: Request,
        channel: str,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(link=channel)
            channel_service.unsubscribe_channel(request.user, channel_post_entity=channels_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})
        except UserIsNotSubscribed as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChannelExistsView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        channel: str,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(link=channel)
            channel_exists = channel_service.channel_exists(channels_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})

        return Response(data={'exists': channel_exists})
