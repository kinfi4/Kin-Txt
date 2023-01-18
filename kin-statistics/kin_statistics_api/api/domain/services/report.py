import logging

from django.contrib.auth.models import User

from api.domain.entities.report import (
    ReportIdentificationEntity,
    ReportPutEntity,
    StatisticalReport,
    WordCloudReport,
)
from api.exceptions import ReportAccessForbidden
from api.infrastructure.interfaces import IReportRepository
from api.infrastructure.repositories.reports import ReportsAccessManagementRepository


class ManagingReportsService:
    def __init__(
        self,
        reports_access_management_repository: ReportsAccessManagementRepository,
        reports_repository: IReportRepository,
    ) -> None:
        self._access_management_repository = reports_access_management_repository
        self._reports_repository = reports_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_reports_names(self, user: User) -> list[ReportIdentificationEntity]:
        user_reports_ids = self._access_management_repository.get_user_report_ids(user.id)
        self._logger.info(f'[ManagingReportsService] got user_reports for user: {user.username}')

        return self._reports_repository.get_report_names(user_reports_ids)

    def set_report_name(self, user: User, report_put_entity: ReportPutEntity) -> ReportIdentificationEntity:
        self._check_user_access(user, report_ids=[report_put_entity.report_id])

        self._logger.info(
            f'[ManagingReportsService] '
            f'updating report {report_put_entity.report_id} with new name: {report_put_entity.name}'
        )

        new_report = self._reports_repository.update_report_name(report_put_entity.report_id, report_put_entity.name)

        return ReportIdentificationEntity(
            report_id=new_report.report_id,
            name=new_report.name,
            report_type=new_report.report_type,
        )

    def get_user_detailed_report(self, user: User, report_id: int) -> StatisticalReport | WordCloudReport:
        self._check_user_access(user, report_ids=[report_id])

        return self._reports_repository.get_report(report_id)

    def count_user_reports_generations(self, user: User) -> int:
        return self._access_management_repository.count_user_reports_synchronous_generations(user_id=user.id)

    def delete_report(self, user: User, report_id: int) -> None:
        self._check_user_access(user, [report_id])

        self._reports_repository.delete_report(report_id=report_id)
        self._access_management_repository.delete_report(report_id=report_id)

    def _check_user_access(self, user: User, report_ids: list[int]) -> None:
        user_reports = self._access_management_repository.get_user_report_ids(user_id=user.id)

        if not all([report_id in user_reports for report_id in report_ids]):
            raise ReportAccessForbidden('You do not have permission for this report!')
