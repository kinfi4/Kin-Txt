from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, Response, status
from starlette.responses import FileResponse

from kin_model_types import Settings
from kin_model_types.containers import Container
from kin_model_types.domain.entities import User
from kin_model_types.exceptions import UserModelNotFoundException
from kin_model_types.infrastructure.repositories import ModelRepository
from kin_model_types.views.helpers.auth import get_current_user

router = APIRouter(prefix="/blobs")


@router.get("/get-model-binaries/{model_code}")
@inject
def get_model_binaries(
    model_code: str,
    current_user: User = Depends(get_current_user),
    model_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    try:
        model = model_repository.get_model(model_code, current_user.username)
    except UserModelNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Model not found")

    models_storage_path = Settings().models_storage_path
    return FileResponse(
        model.get_model_binaries_path(models_storage_path),
        media_type="application/octet-stream",
        filename=f"{model_code}",
    )


@router.get("/get-tokenizer-binaries/{model_code}")
@inject
def get_model_binaries(
    model_code: str,
    current_user: User = Depends(get_current_user),
    model_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    try:
        model = model_repository.get_model(model_code, current_user.username)
    except UserModelNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Tokenizer not found")

    models_storage_path = Settings().models_storage_path
    return FileResponse(
        model.get_tokenizer_binaries_path(models_storage_path),
        media_type="application/octet-stream",
        filename=f"tokenizer-{model_code}",
    )
