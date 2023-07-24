from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, status
from fastapi.responses import Response

from kin_reports_generation.containers import Container
from kin_reports_generation.domain.entities import User, ModelEntity, ModelValidationEntity, UpdateModelEntity
from kin_reports_generation.views.helpers.auth import get_current_user
from kin_reports_generation.domain.services.model import ModelService
from kin_reports_generation.infrastructure.repositories import ModelRepository
from kin_reports_generation.exceptions import BaseValidationError, UserModelNotFoundException

router = APIRouter(prefix="/models")


@router.get("", response_model=list[ModelEntity])
@inject
def get_user_models(
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    return models_repository.get_user_models(current_user.username)


@router.post("")
@inject
def validate_and_save_model(
    model: ModelValidationEntity = Depends(ModelValidationEntity.as_form),
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        models_service.validate_and_save(current_user.username, model)
    except BaseValidationError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/{model_id}")
@inject
def update_model(
    model_id: str,
    model: UpdateModelEntity = Depends(UpdateModelEntity.as_form),
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        models_service.update_model(current_user.username, model_id, model)
    except BaseValidationError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_200_OK)


@router.get("/{model_id}", response_model=ModelEntity, status_code=status.HTTP_200_OK)
@inject
def get_model(
    model_id: str,
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    try:
        return models_repository.get_model(model_id, username=current_user.username)
    except UserModelNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{model_id}")
@inject
def delete_model(
    model_id: str,
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.repositories.model_repository]),
):
    models_repository.delete_model(model_id, username=current_user.username)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
