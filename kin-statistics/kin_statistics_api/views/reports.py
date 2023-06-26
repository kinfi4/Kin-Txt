import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from kin_news_core.exceptions import KinNewsCoreException
from kin_statistics_api.containers import Container
from kin_statistics_api.domain.entities import GenerateReportEntity, ReportPutEntity, User
from kin_statistics_api.domain.services import ManagingReportsService, UserService
from kin_statistics_api.exceptions import ReportAccessForbidden
from kin_statistics_api.views.helpers.auth import get_current_user

_logger = logging.getLogger(__name__)


router = APIRouter(prefix='/reports')


@router.get('')
@inject
def get_reports(
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    report_identities = reports_service.get_user_reports_names(current_user.username)

    return JSONResponse(content={'reports': [report.dict(by_alias=True, with_serialization=True) for report in report_identities]})


@router.post('')
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
                'errors': f'Sorry, but you can not generate more than '
                          f'{max_synchronous_reports_generation} at the same time'
            }
        )

    try:
        _logger.info('Creating Celery job for report generation...')
        reports_service.start_report_generation(current_user, generate_report_entity)
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'errors': str(err)})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': 'Generating report process started successfully!'})


@router.get('/{report_id}')
@inject
def get_report_details(
    report_id: int,
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    try:
        report = reports_service.get_user_detailed_report(current_user.username, report_id)
    except ReportAccessForbidden:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'errors': 'You do not have rights to this report!'})
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'errors': str(err)})

    return JSONResponse(content=report.dict(by_alias=True, with_serialization=True))


@router.put('/{report_id}')
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
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'errors': 'You do not have rights to this report!'})
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'errors': str(err)})

    return JSONResponse(content=report_identity.dict(by_alias=True, with_serialization=True))


@router.delete('/{report_id}')
@inject
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    reports_service: ManagingReportsService = Depends(Provide[Container.services.managing_reports_service]),
):
    try:
        reports_service.delete_report(current_user.username, report_id)
    except ReportAccessForbidden:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'errors': 'You do not have rights to this report!'})
    except KinNewsCoreException as err:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'errors': str(err)})

    return Response(status_code=status.HTTP_204_NO_CONTENT)
