import logging

from kin_statistics_api.domain.entities.report import (
    ReportIdentificationEntity,
    StatisticalReport,
    WordCloudReport,
)
from kin_statistics_api.exceptions import ReportAccessForbidden
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.infrastructure.repositories.access_management import ReportsAccessManagementRepository


class ManagingReportsService:
    def __init__(
        self,
        reports_access_management_repository: ReportsAccessManagementRepository,
        reports_repository: IReportRepository,
    ) -> None:
        self._access_management_repository = reports_access_management_repository
        self._reports_repository = reports_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_reports_names(self, username: str) -> list[ReportIdentificationEntity]:
        user_reports_ids = self._access_management_repository.get_user_report_ids(username)
        self._logger.info(f'[ManagingReportsService] got user_reports for user: {username}')

        return self._reports_repository.get_report_names(user_reports_ids)

    def set_report_name(self, username: str, report_name: str, report_id: int) -> ReportIdentificationEntity:
        self._check_user_access(username, report_ids=[report_id])

        self._logger.info(
            f'[ManagingReportsService] '
            f'updating report {report_id} with new name: {report_name}'
        )

        new_report = self._reports_repository.update_report_name(report_id, report_name)

        return ReportIdentificationEntity(
            report_id=new_report.report_id,
            name=new_report.name,
            report_type=new_report.report_type,
        )

    def get_user_detailed_report(self, username: str, report_id: int) -> StatisticalReport | WordCloudReport:
        self._check_user_access(username, report_ids=[report_id])

        return self._reports_repository.get_report(report_id)

    def count_user_reports_generations(self, username: str) -> int:
        return self._access_management_repository.count_user_reports_synchronous_generations(username=username)

    def delete_report(self, username: str, report_id: int) -> None:
        self._check_user_access(username, [report_id])

        self._reports_repository.delete_report(report_id=report_id)
        self._access_management_repository.delete_report(report_id=report_id)

    def _check_user_access(self, username: str, report_ids: list[int]) -> None:
        user_reports = self._access_management_repository.get_user_report_ids(username=username)

        if not all([report_id in user_reports for report_id in report_ids]):
            raise ReportAccessForbidden('You do not have permission for this report!')
