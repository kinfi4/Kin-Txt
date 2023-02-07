from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, APIRouter, Response, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse

from kin_statistics_api.containers import Container
from kin_statistics_api.domain.entities.user import User
from kin_statistics_api.domain.use_cases import file_generator_user_case
from kin_statistics_api.exceptions import ReportDataNotFound
from kin_statistics_api.views.helpers.auth import get_current_user
from kin_statistics_api.domain.services import ReportDataSaver

router = APIRouter(prefix='/reports-data')


@router.post('/save')
@inject
def get_report_data(
    report_id: int = Form(...),
    file_type: str = Form(...),
    report_data_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    data_saver_service: ReportDataSaver = Depends(Provide[Container.services.reports_data_saver]),
):
    if not current_user.internal_user:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data_saver_service.save_report_data(report_id, file_type, report_data_file.file)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'errors': ['Invalid document type.']})
    except ReportDataNotFound:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{report_id}')
@inject
def get_report_data(
    report_id: int,
    export_type: Optional[str],
    current_user: User = Depends(get_current_user),
):
    try:
        if not export_type:
            raise ReportDataNotFound()

        use_case = file_generator_user_case(export_type)
        file, filename = use_case.get_file(current_user, report_id)

        return StreamingResponse(
            file,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
            }
        )
    except ReportDataNotFound:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
