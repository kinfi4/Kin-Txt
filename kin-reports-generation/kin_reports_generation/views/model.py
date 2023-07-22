from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, Response, status, UploadFile, File, Form, Body
from fastapi.responses import StreamingResponse, Response

from kin_reports_generation.containers import Container
from kin_reports_generation.domain.entities import User, ModelEntity, ModelValidationEntity
from kin_reports_generation.views.helpers.auth import get_current_user
from kin_reports_generation.domain.services.model import ModelService
from kin_reports_generation.infrastructure.repositories import ModelRepository
from kin_reports_generation.exceptions import BaseValidationError

router = APIRouter(prefix="/models")


@router.get("", response_model=list[ModelEntity])
@inject
def get_user_models(
    current_user: User = Depends(get_current_user),
    models_repository: ModelRepository = Depends(Provide[Container.services.templates_service]),
):
    return models_repository.get_user_models(current_user.username)


@router.post("validate-and-save")
@inject
def validate_and_save_model(
    model: ModelValidationEntity = Depends(ModelValidationEntity.as_form),
    current_user: User = Depends(get_current_user),
    models_service: ModelService = Depends(Provide[Container.services.domain_services.models_service]),
):
    try:
        models_service.validate_and_save(current_user.username, model)
    except BaseValidationError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_201_CREATED)
