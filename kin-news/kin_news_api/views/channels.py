from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError

from domain.entities import ChannelPostEntity
from kin_news_api import Settings
from kin_news_api.views.helpers.auth import get_current_user
from kin_news_api.domain.entities import UserEntity
from kin_news_api.containers import Container
from kin_news_api.domain.services import ChannelService
from kin_news_api.exceptions import UserMaxSubscriptionsExceeded, UserIsNotSubscribed
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.utils import pydantic_errors_prettifier

api_router = APIRouter()


@api_router.get("/channels")
@inject
async def get_user_channels(
    current_user: UserEntity = Depends(get_current_user),
    channel_service: ChannelService = Depends(Provide[Container.domain_services.channel_service]),
):
    channels = await channel_service.get_user_channels(current_user.username)
    channels_serialized = [channel.dict(by_alias=True) for channel in channels]

    return JSONResponse(content=channels_serialized)


@api_router.post("/channels")
@inject
async def subscribe_user(
    channel_data: ChannelPostEntity,
    current_user: UserEntity = Depends(get_current_user),
    channel_service: ChannelService = Depends(Provide[Container.domain_services.channel_service]),
    config: Settings = Depends(Provide[Container.config]),
):
    try:
        channel = await channel_service.subscribe_user(current_user.username, channel_data)
    except UserMaxSubscriptionsExceeded:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "errors": f"We are sorry, but you have exceeded maximum number of subscriptions. "
                          f"You may subscribe only up to {config.max_user_subscriptions_count} at the same time."
            }
        )
    except InvalidChannelURLError as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return JSONResponse(content=channel.dict(by_alias=True))


@api_router.delete("/channels/{channel}")
@inject
async def unsubscribe_user(
    channel: str,
    current_user: UserEntity = Depends(get_current_user),
    channel_service: ChannelService = Depends(Provide[Container.domain_services.channel_service]),
):
    try:
        channels_entity = ChannelPostEntity(link=channel)

        await channel_service.unsubscribe_channel(current_user.username, channel_post_entity=channels_entity)
    except ValidationError as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": pydantic_errors_prettifier(err.errors())})
    except UserIsNotSubscribed as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


@api_router.get("/channels/exists/{channel:path}")
@inject
async def check_channel_exists(
    channel: str,
    _: UserEntity = Depends(get_current_user),
    channel_service: ChannelService = Depends(Provide[Container.domain_services.channel_service]),
):
    try:
        channels_entity = ChannelPostEntity(link=channel)
        channel_exists = await channel_service.channel_exists(channels_entity)
    except ValidationError as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": pydantic_errors_prettifier(err.errors())})

    return JSONResponse(content={"exists": channel_exists})
