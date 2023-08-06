from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status

from kin_reports_generation.containers import Container
from kin_reports_generation.exceptions import UserTemplateNotFoundException
from kin_reports_generation.views.helpers.auth import get_current_user
from kin_reports_generation.domain.entities import User, VisualizationTemplate
from kin_reports_generation.infrastructure.repositories import VisualizationTemplateRepository

router = APIRouter(prefix="/visualization-template")


@router.get("", response_model=list[VisualizationTemplate], status_code=status.HTTP_200_OK)
@inject
def get_templates(
    current_user: User = Depends(get_current_user),
    visualization_template_repository: VisualizationTemplateRepository = Depends(Provide[Container.repositories.visualization_template_repository]),
):
    return visualization_template_repository.get_user_templates(current_user.username)


@router.post("")
@inject
def create_template(
    template: VisualizationTemplate,
    current_user: User = Depends(get_current_user),
    visualization_template_repository: VisualizationTemplateRepository = Depends(Provide[Container.repositories.visualization_template_repository]),
):
    visualization_template_repository.save_template(current_user.username, template)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{template_id}", response_model=VisualizationTemplate, status_code=status.HTTP_200_OK)
@inject
def get_template(
    template_id: str,
    current_user: User = Depends(get_current_user),
    visualization_template_repository: VisualizationTemplateRepository = Depends(Provide[Container.repositories.visualization_template_repository]),
):
    try:
        return visualization_template_repository.get_template(template_id, current_user.username)
    except UserTemplateNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{template_id}")
@inject
def delete_template(
    template_id: str,
    current_user: User = Depends(get_current_user),
    visualization_template_repository: VisualizationTemplateRepository = Depends(Provide[Container.repositories.visualization_template_repository]),
):
    try:
        visualization_template_repository.delete_template(current_user.username, template_id)
    except UserTemplateNotFoundException:
        pass

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{template_id}")
@inject
def update_template(
    template_id: str,
    template: VisualizationTemplate,
    current_user: User = Depends(get_current_user),
    visualization_template_repository: VisualizationTemplateRepository = Depends(Provide[Container.repositories.visualization_template_repository]),
):
    try:
        visualization_template_repository.update_template(template_id, current_user.username, template)
    except UserTemplateNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)
