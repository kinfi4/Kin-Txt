from typing import Callable

from dependency_injector.wiring import Provide, inject
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.services import IReportFileGenerator
from api.exceptions import ReportDataNotFound
from config.containers import Container


class GetReportDataView(APIView):
    @inject
    def get(
        self,
        request: Request,
        report_id: int,
        report_data_use_case: Callable[..., IReportFileGenerator] = Provide[Container.use_cases.report_data_use_case],
    ):
        file_type = request.query_params.get('type')

        try:
            if not file_type:
                raise ReportDataNotFound()

            use_case = report_data_use_case(file_type)
            file, filename = use_case.get_file(report_id)

            return StreamingHttpResponse(
                file,
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                }
            )
        except ReportDataNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
