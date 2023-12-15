import math
import logging
from datetime import datetime

from kin_txt_core.messaging import AbstractEventProducer
from kin_txt_core.pagination import PaginatedDataEntity

from kin_statistics_api.domain.entities import (
    ReportIdentificationEntity,
    StatisticalReport,
    WordCloudReport,
    GenerateReportEntity,
    BaseReport,
    User,
    ReportsFetchSettings,
)
from kin_statistics_api.domain.events import GenerateReportRequestOccurred
from kin_statistics_api.exceptions import ReportAccessForbidden, ReportNotFound
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.infrastructure.repositories.access_management import ReportsAccessManagementRepository
from kin_statistics_api.constants import REPORTS_BUILDER_EXCHANGE, ReportTypes, ReportProcessingResult
from kin_statistics_api.constants import ITEMS_PER_PAGE


class ManagingReportsService:
    def __init__(
        self,
        reports_access_management_repository: ReportsAccessManagementRepository,
        reports_repository: IReportRepository,
        events_producer: AbstractEventProducer,
    ) -> None:
        self._iam_repository = reports_access_management_repository
        self._reports_repository = reports_repository
        self._events_producer = events_producer
        self._logger = logging.getLogger(self.__class__.__name__)

    def report_processing_finished(self, username: str, report: BaseReport) -> None:
        self._iam_repository.set_user_finished_report_generation(username)

        if not self._reports_repository.report_exists(report.report_id):
            return  # that means user has deleted report before it was finished

        self.save_report(report)

    def start_report_generation(self, user: User, generation_entity: GenerateReportEntity) -> None:
        self._iam_repository.set_user_began_report_generation(user.username)
        report_id = self._iam_repository.create_new_user_report(user.username)

        empty_report = self._build_empty_report(report_id, generation_entity)

        self.save_report(empty_report)

        generation_event = GenerateReportRequestOccurred(
            **generation_entity.dict(),
            username=user.username,
            report_id=report_id,
        )

        self._events_producer.publish(
            REPORTS_BUILDER_EXCHANGE,
            [generation_event],
        )

    def update_report_status(self, report_id: int, new_status: ReportProcessingResult) -> None:
        self._logger.info(f"Updating status for report {report_id} to: {new_status}")

        if not self._reports_repository.report_exists(report_id):
            return  # that means user has deleted report before it was finished

        self._reports_repository.update_report_status(report_id, new_status)

    def save_report(self, report: BaseReport) -> None:
        self._logger.info(f"Saving report {report.report_id} with status: {report.processing_status}")

        self._reports_repository.save_user_report(report)

    def get_user_reports_names(self, username: str, fetch_settings: ReportsFetchSettings | None = None) -> PaginatedDataEntity[ReportIdentificationEntity]:
        user_reports_ids = self._iam_repository.get_user_report_ids(username)
        self._logger.info(f"[ManagingReportsService] got user_reports for user: {username}")

        report_entities = self._reports_repository.get_report_names(user_reports_ids, apply_settings=fetch_settings)
        total_reports_count = self._reports_repository.get_total_reports_count(filters=fetch_settings)

        return PaginatedDataEntity(
            data=report_entities,
            total_pages=math.ceil(total_reports_count / ITEMS_PER_PAGE),
            page=fetch_settings.page if fetch_settings else 0,
        )

    def set_report_name(self, username: str, report_name: str, report_id: int) -> ReportIdentificationEntity:
        self._check_user_access(username, report_ids=[report_id])

        self._logger.info(
            f"[ManagingReportsService] "
            f"updating report {report_id} with new name: {report_name}"
        )

        new_report = self._reports_repository.update_report_name(report_id, report_name)

        return ReportIdentificationEntity(
            report_id=new_report.report_id,
            name=new_report.name,
            report_type=new_report.report_type,
            generation_date=new_report.generation_date,
            processing_status=new_report.processing_status,
        )

    def get_user_detailed_report(self, username: str, report_id: int) -> StatisticalReport | WordCloudReport:
        self._check_user_access(username, report_ids=[report_id])

        return self._reports_repository.get_report(report_id)

    def count_user_reports_generations(self, username: str) -> int:
        return self._iam_repository.count_user_reports_synchronous_generations(username=username)

    def delete_report(self, username: str, report_id: int) -> None:
        self._check_user_access(username, [report_id])

        self._reports_repository.delete_report(report_id=report_id)
        self._iam_repository.delete_report(report_id=report_id)

    def _check_user_access(self, username: str, report_ids: list[int]) -> None:
        user_reports = self._iam_repository.get_user_report_ids(username=username)

        if not all([report_id in user_reports for report_id in report_ids]):
            raise ReportAccessForbidden("You do not have permission for this report!")

    def _build_empty_report(self, report_id: int, generation_entity: GenerateReportEntity) -> BaseReport:
        return BaseReport(
            report_id=report_id,
            report_type=generation_entity.report_type,
            processing_status=ReportProcessingResult.NEW,
            name=generation_entity.name,
            generation_date=datetime.now(),
        )