from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from kin_news_api.domain.services import MessageService, ChannelService
from kin_news_api.domain.entities import UserEntity
from kin_news_api.views.helpers.auth import get_current_user
from kin_news_api.containers import Container
from kin_news_api.exceptions import InvalidURIParams, UserIsNotSubscribed, UserAlreadyFetchingNews
from kin_news_core.exceptions import TelegramIsUnavailable

api_router = APIRouter(prefix="")


@api_router.get("/messages")
@inject
async def get_messages(
    start_time: str,
    end_time: str,
    current_user: UserEntity = Depends(get_current_user),
    messages_service: MessageService = Depends(Provide[Container.domain_services.message_service]),
    channel_service: ChannelService = Depends(Provide[Container.domain_services.channel_service]),
):
    try:
        start_time, end_time = _parse_query_params(start_time, end_time)
        user_channels = await channel_service.get_user_channels(current_user.username)

        messages = await messages_service.get_user_posts(
            current_user.username,
            user_channels,
            start_time=start_time,
            end_time=end_time,
        )

    except UserIsNotSubscribed:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errors": "User is not subscribed"})
    except InvalidURIParams as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})
    except UserAlreadyFetchingNews as err:
        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"errors": str(err)})
    except TelegramIsUnavailable as err:
        hours_to_wait = err.seconds_to_wait // 3600
        minutes_to_wait = (err.seconds_to_wait - hours_to_wait * 3600) // 60
        seconds_to_wait = (err.seconds_to_wait - hours_to_wait * 3600) - minutes_to_wait * 60

        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "errors": f"Telegram is unavailable, we need {hours_to_wait} hours, {minutes_to_wait} minutes "
                          f"and {seconds_to_wait} seconds to wait. We are sorry for this issue!"
            }
        )

    messages_serialized = [message.dict(by_alias=True) for message in messages]
    return JSONResponse(content={
        'messages': messages_serialized,
        'messagesCount': len(messages_serialized),
    })


def _parse_query_params(st_time_string: str, end_time_string: str) -> tuple[datetime | None, datetime | None]:
    try:
        if st_time_string is not None:
            start_timestamp = int(st_time_string) // 1000
            start_time = datetime.fromtimestamp(start_timestamp)
        else:
            start_time = datetime.now() - timedelta(hours=5)

        if end_time_string is not None:
            end_timestamp = int(end_time_string) // 1000
            end_time = datetime.fromtimestamp(end_timestamp)
        else:
            end_time = datetime.now()

        if start_time > end_time:
            raise InvalidURIParams("Start time must be earlier than end time.")

        if (end_time - start_time).total_seconds() > 3600 * 24:
            raise InvalidURIParams("You can not fetch data for such long period of time!")
    except ValueError:
        raise InvalidURIParams("You have passed invalid query params! Offset/End time must be integers representing timestamp")

    return start_time, end_time
