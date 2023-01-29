from typing import Callable, Optional

from dependency_injector.wiring import inject
from fastapi import Depends, APIRouter, Response, status
from fastapi.responses import StreamingResponse

from kin_statistics_api.domain.entities.user import User
from kin_statistics_api.domain.use_cases import file_generator_user_case
from kin_statistics_api.exceptions import ReportDataNotFound
from kin_statistics_api.views.helpers.auth import get_current_user

router = APIRouter(prefix='/reports-data')


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
