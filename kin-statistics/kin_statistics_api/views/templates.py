import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse, Response

from kin_news_core.exceptions import KinNewsCoreException
from kin_statistics_api.containers import Container
from kin_statistics_api.domain.entities import User, GenerationTemplate
from kin_statistics_api.domain.services import GenerationTemplateService
from kin_statistics_api.exceptions import GenerationTemplateNotFound
from kin_statistics_api.views.helpers.auth import get_current_user

_logger = logging.getLogger(__name__)


router = APIRouter(prefix="/templates")


@router.get("")
@inject
def get_user_templates(
    current_user: User = Depends(get_current_user),
    templates_service: GenerationTemplateService = Depends(Provide[Container.services.templates_service]),
):
    templates_names = templates_service.get_user_template_names(current_user.username)
    return JSONResponse(content={"templates": templates_names})


@router.post("")
@inject
def generate_report_request(
    generation_template: GenerationTemplate,
    current_user: User = Depends(get_current_user),
    templates_service: GenerationTemplateService = Depends(Provide[Container.services.templates_service]),
):
    templates_service.save_user_template(current_user.username, generation_template)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{template_id}", response_model=GenerationTemplate, status_code=status.HTTP_200_OK)
@inject
def get_report_details(
    template_id: str,
    current_user: User = Depends(get_current_user),
    templates_service: GenerationTemplateService = Depends(Provide[Container.services.templates_service]),
):
    try:
        template = templates_service.load_user_template(current_user.username, template_id)
    except GenerationTemplateNotFound:
        raise HTTPException(status_code=404, detail="Generation Template not found.")

    return template


@router.delete("/{template_id}")
@inject
def delete_report(
    template_id: str,
    current_user: User = Depends(get_current_user),
    templates_service: GenerationTemplateService = Depends(Provide[Container.services.templates_service]),
):
    try:
        templates_service.delete_user_template(current_user.username, template_id)
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return Response(status_code=status.HTTP_204_NO_CONTENT)
