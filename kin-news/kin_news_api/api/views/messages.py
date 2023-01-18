import logging
from datetime import datetime, timedelta
from typing import Optional

from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.services import ChannelService, MessageService
from api.exceptions import (
    InvalidURIParams,
    UserAlreadyFetchingNews,
    UserIsNotSubscribed,
)
from config.containers import Container
from kin_news_core.auth import JWTAuthentication
from kin_news_core.exceptions import TelegramIsUnavailable

_logger = logging.getLogger(__name__)


class MessagesView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        message_service: MessageService = Provide[Container.domain_services.message_service],
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:

        try:
            start_time, end_time = self._parse_query_params(request)
            user_channels = channel_service.get_user_channels(request.user)

            messages = message_service.get_user_posts(request.user.id, user_channels, start_time=start_time, end_time=end_time)
        except UserIsNotSubscribed:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except InvalidURIParams as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})
        except UserAlreadyFetchingNews as err:
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS, data={'errors': str(err)})
        except TelegramIsUnavailable as err:
            hours_to_wait = err.seconds_to_wait // 3600
            minutes_to_wait = (err.seconds_to_wait - hours_to_wait*3600) // 60
            seconds_to_wait = (err.seconds_to_wait - hours_to_wait*3600) - minutes_to_wait*60

            return Response(
                status=status.HTTP_429_TOO_MANY_REQUESTS,
                data={'errors': f'Telegram is unavailable, we need {hours_to_wait} hours, {minutes_to_wait} minutes '
                                f'and {seconds_to_wait} seconds to wait. We are sorry for this issue!'}
            )

        messages_serialized = [message.dict(by_alias=True) for message in messages]
        return Response(data={
            'messages': messages_serialized,
            'messagesCount': len(messages_serialized),
        })

    @staticmethod
    def _parse_query_params(request: Request) -> tuple[Optional[datetime], Optional[datetime]]:
        start_time_str = request.query_params.get('start_time')
        end_time_str = request.query_params.get('end_time')

        try:
            if start_time_str is not None:
                start_timestamp = int(start_time_str) // 1000
                start_time = datetime.fromtimestamp(start_timestamp)
            else:
                start_time = datetime.now() - timedelta(hours=5)

            if start_time_str is not None:
                end_timestamp = int(end_time_str) // 1000
                end_time = datetime.fromtimestamp(end_timestamp)
            else:
                end_time = datetime.now()

            if start_time > end_time:
                raise InvalidURIParams('Start time must be earlier than end time.')

            if (end_time - start_time).total_seconds() > 3600 * 24:
                raise InvalidURIParams('You can not fetch data for such long period of time!')
        except ValueError as err:
            _logger.info(f'Invalid query params passed: {err}')
            raise InvalidURIParams('You have passed invalid query params! Offset/End time must be integers representing timestamp')

        return start_time, end_time
