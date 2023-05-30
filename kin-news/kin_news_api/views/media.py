import os

from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from kin_news_api.settings import Settings
from kin_news_api.domain.entities import UserEntity
from kin_news_api.containers import Container
from kin_news_api.views.helpers.auth import get_current_user

media_router = APIRouter()

@media_router.get("/media/profile_photos/{file_name}")
@inject
async def get_media(
    file_name: str,
    _: UserEntity = Depends(get_current_user),
    config: Settings = Depends(Provide[Container.config])
):
    profile_pictures_path = os.path.join(config.media_root, "profile_photos")
    file_path = os.path.join(profile_pictures_path, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(file_path)
