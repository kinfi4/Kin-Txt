from fastapi import APIRouter

from kin_news_api.constants import API_ROUTE_PATH
from kin_news_api.views.ratings import api_router as ratings_router
from kin_news_api.views.accounts import api_router as users_router
from kin_news_api.views.messages import api_router as news_router
from kin_news_api.views.channels import api_router as channels_router

api_router = APIRouter(prefix=API_ROUTE_PATH)

api_router.include_router(ratings_router)
api_router.include_router(users_router)
api_router.include_router(news_router)
api_router.include_router(channels_router)
