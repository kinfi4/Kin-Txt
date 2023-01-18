import logging

from dependency_injector.wiring import Provide, inject
from django.conf import settings
from pydantic import ValidationError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response

from api.domain.entities import GenerateReportEntity, ReportPutEntity
from api.domain.services import ManagingReportsService, UserService
from api.domain.services.reports_generator.generate_report_usecase import (
    generate_report_use_case,
)
from api.exceptions import ReportAccessForbidden
from config.constants import DEFAULT_DATE_FORMAT
from config.containers import Container
from kin_news_core.auth import JWTAuthentication
from kin_news_core.exceptions import KinNewsCoreException
from kin_news_core.utils import pydantic_errors_prettifier

_logger = logging.getLogger(__name__)


class ReportsListView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @inject
    def get(
        self,
        request: Request,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        report_identities = reports_service.get_user_reports_names(request.user)

        return Response(
            data={'reports': [report.dict(by_alias=True) for report in report_identities]}
        )

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.services.user_service],
    ) -> Response:
        if user_service.count_user_reports_generations(request.user.id) >= settings.MAX_SYNCHRONOUS_REPORTS_GENERATION:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={
                    'errors': f'Sorry, but you can not generate more than '
                              f'{settings.MAX_SYNCHRONOUS_REPORTS_GENERATION} at the same time'
                }
            )

        try:
            generate_report = GenerateReportEntity(
                start_date=request.data['startDate'],
                end_date=request.data['endDate'],
                channel_list=request.data['channels'],
                report_type=request.data['reportType'],
            )

            _logger.info('Creating Celery job for report generation...')

            use_case = generate_report_use_case(generate_report.report_type)

            use_case.delay(
                start_date=generate_report.start_date.strftime(DEFAULT_DATE_FORMAT),
                end_date=generate_report.end_date.strftime(DEFAULT_DATE_FORMAT),
                channel_list=generate_report.channel_list,
                user_id=request.user.id,
            )
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})
        except KinNewsCoreException as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(status=status.HTTP_202_ACCEPTED, data={'message': 'Generating report process started successfully!'})


class ReportsSingleView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @inject
    def get(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            report = reports_service.get_user_detailed_report(request.user, report_id)
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'You do not have rights to this report!'})
        except KinNewsCoreException as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(data=report.dict(by_alias=True))

    @inject
    def put(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            report_put_entity = ReportPutEntity(**request.data, report_id=report_id)
            report_identity = reports_service.set_report_name(request.user, report_put_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'User does not have rights to this report!'})
        except KinNewsCoreException as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(data=report_identity.dict(by_alias=True))

    @inject
    def delete(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            reports_service.delete_report(request.user, report_id)
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'User does not have rights to this report!'})
        except KinNewsCoreException as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(status=status.HTTP_204_NO_CONTENT)
