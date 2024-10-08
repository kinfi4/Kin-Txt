import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from kin_txt_core.pagination import PaginatedDataEntity

from kin_txt_core.exceptions import KinNewsCoreException
from kin_statistics_api.containers import Container
from kin_statistics_api.domain.entities import (
    GenerateReportEntity,
    ReportPutEntity,
    User,
    ReportsFetchSettings,
    ReportIdentificationEntity,
    StatisticalReport,
    WordCloudReport,
    BaseReport,
)
from kin_statistics_api.domain.services import ManagingReportsService, UserService
from kin_statistics_api.exceptions import ReportAccessForbidden
from kin_statistics_api.views.helpers.auth import get_current_user

_logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports")


@router.get("", response_model=PaginatedDataEntity[ReportIdentificationEntity])
@inject
def get_reports(
    fetch_settings: ReportsFetchSettings = Depends(),
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    return reports_service.get_reports_preview(current_user.username, fetch_settings=fetch_settings)


@router.post("")
@inject
def generate_report_request(
    generate_report_entity: GenerateReportEntity,
    current_user: User = Depends(get_current_user),
    max_synchronous_reports_generation: int = Depends(Provide[Container.config.max_synchronous_reports_generation]),
    user_service: UserService = Depends(Provide[Container.services.user_service]),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    if user_service.count_user_reports_generations(current_user.username) >= max_synchronous_reports_generation:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "errors": f"Sorry, but you can not generate more than "
                          f"{max_synchronous_reports_generation} at the same time"
            }
        )

    try:
        reports_service.start_report_generation(current_user, generate_report_entity)
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"message": "Generating report process started successfully!"},
    )


@router.get("/{report_id}", response_model=BaseReport | StatisticalReport | WordCloudReport)
@inject
def get_report_details(
    report_id: int,
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    try:
        report = reports_service.get_detailed_report(current_user.username, report_id)
    except ReportAccessForbidden:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"errors": "You do not have rights to this report!"},
        )
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return report


@router.put("/{report_id}", response_model=StatisticalReport | WordCloudReport)
@inject
def update_report(
    report_id: int,
    report_put_entity: ReportPutEntity,
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    try:
        report_identity = reports_service.set_report_name(current_user.username, report_put_entity.name, report_id)
    except ReportAccessForbidden:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"errors": "You do not have rights to this report!"},
        )
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return report_identity


@router.delete("/{report_id}")
@inject
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    try:
        reports_service.delete_report(current_user.username, report_id)
    except ReportAccessForbidden:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"errors": "You do not have rights to this report!"},
        )
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": str(err)})

    return Response(status_code=status.HTTP_204_NO_CONTENT)
