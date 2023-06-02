from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from kin_news_api.exceptions import ChannelDoesNotExists
from kin_news_api.domain.entities import RatePostEntity, UserEntity
from kin_news_api.domain.services import RatingsService
from kin_news_api.containers import Container
from kin_news_api.views.helpers.auth import get_current_user


api_router = APIRouter()


@api_router.get("/channels/rates")
@inject
async def get_user_rates(
    channel: str,
    current_user: UserEntity = Depends(get_current_user),
    rating_service: RatingsService = Depends(Provide[Container.domain_services.rating_service]),
):
    ratings = await rating_service.get_channel_rating_stats(current_user.username, channel)

    return JSONResponse(content=ratings.dict(by_alias=True))


@api_router.post("/channels/rates")
@inject
async def rate_channel(
    rate_data: RatePostEntity,
    current_user: UserEntity = Depends(get_current_user),
    rating_service: RatingsService = Depends(Provide[Container.domain_services.rating_service]),
):
    try:
        rating = await rating_service.rate_channel(current_user.username, rate_data)
    except ChannelDoesNotExists as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return JSONResponse(content=rating.dict(by_alias=True))
