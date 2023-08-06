from typing import cast

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, status
from fastapi.responses import Response, JSONResponse
from celery import Task

from kin_reports_generation.containers import Container
from kin_reports_generation.domain.entities import User, ModelEntity, CreateModelEntity, UpdateModelEntity
from kin_reports_generation.tasks import validate_model
from kin_reports_generation.views.helpers.auth import get_current_user
from kin_reports_generation.domain.services.model import ModelService
from kin_reports_generation.infrastructure.repositories import ModelRepository
from kin_reports_generation.exceptions import BaseValidationError, UserModelNotFoundException, UnsupportedModelTypeError

validate_model = cast(Task, validate_model)

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
    model: CreateModelEntity = Depends(CreateModelEntity.as_form),
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.domain_services.models_service]),
):
    try:
        model_to_validate = models_service.prepare_model_for_validation(current_user.username, model)
        validate_model.delay(model_to_validate.dict())
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
        validation_needed, model_to_validate = models_service.update_model(current_user.username, model_id, model)
        if validation_needed:
            validate_model.delay(model_to_validate.dict())
    except UnsupportedModelTypeError as error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(error)})
    except UserModelNotFoundException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errors": "Model not found."})
    except BaseValidationError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": "Something went wrong."})

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
    try:
        models_repository.delete_model(model_id, username=current_user.username)
    except UserModelNotFoundException:
        pass

    return Response(status_code=status.HTTP_204_NO_CONTENT)
