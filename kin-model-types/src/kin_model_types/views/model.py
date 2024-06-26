from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, status
from fastapi.responses import Response, JSONResponse

from kin_model_types.containers import Container
from kin_model_types.domain.entities import (
    ModelFilters,
    User,
    ModelEntity,
    CreateModelEntity,
    UpdateModelEntity,
)
from kin_model_types.views.helpers.auth import get_current_user
from kin_model_types.domain.services.model import ModelService
from kin_model_types.infrastructure.repositories import ModelRepository
from kin_model_types.exceptions import (
    UserModelNotFoundException,
    ImpossibleToUpdateCustomModelException,
    ImpossibleToDeleteCustomModelException,
    ModelAlreadyExistsException,
)

router = APIRouter(prefix="/models")


@router.get("", response_model=list[ModelEntity])
@inject
def get_user_models(
    filters: ModelFilters = Depends(),
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    return models_repository.get_user_models(current_user.username, filters)


@router.post("")
@inject
def validate_and_save_model(
    model: CreateModelEntity,
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        models_service.validate_model(current_user.username, model)
    except ModelAlreadyExistsException:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"errors": "Model with this code already exists."})

    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/{model_code}")
@inject
def update_model(
    model_code: str,
    model: UpdateModelEntity,
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        models_service.update_model(current_user.username, model_code, model)
    except ImpossibleToUpdateCustomModelException:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"errors": "It's impossible to update custom model."})
    except UserModelNotFoundException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errors": "Model not found."})

    return Response(status_code=status.HTTP_200_OK)


@router.get("/{model_code}")
@inject
def get_model(
    model_code: str,
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    try:
        model_entity = models_repository.get_model(model_code, username=current_user.username)
    except UserModelNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=model_entity.dict(by_alias=True),
    )


@router.delete("/{model_code}")
@inject
def delete_model(
    model_code: str,
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        models_service.delete_model(username=current_user.username, model_code=model_code)
    except ImpossibleToDeleteCustomModelException:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": "It's impossible to delete built-in model."})
    except UserModelNotFoundException:
        pass

    return Response(status_code=status.HTTP_204_NO_CONTENT)
