import math
import logging

from kin_statistics_api.infrastructure.dtos import ReportIdentitiesQueryResult
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
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.infrastructure.repositories.iam import IAMRepository
from kin_statistics_api.constants import REPORTS_BUILDER_EXCHANGE, ReportProcessingResult
from kin_statistics_api.constants import ITEMS_PER_PAGE


class ManagingReportsService:
    def __init__(
        self,
        iam_repository: IAMRepository,
        reports_repository: IReportRepository,
        events_producer: AbstractEventProducer,
    ) -> None:
        self._iam_repository = iam_repository
        self._reports_repository = reports_repository
        self._events_producer = events_producer
        self._logger = logging.getLogger(self.__class__.__name__)

    def report_processing_finished(self, username: str, report: StatisticalReport | WordCloudReport) -> None:
        self._iam_repository.update_user_simultaneous_reports_generation(
            username=username,
            change=-1,
        )

        if not self._reports_repository.report_exists(report.report_id, username):
            return  # that means user has deleted report before it was finished

        self._reports_repository.save_finished_report(report)

    def start_report_generation(self, user: User, generation_entity: GenerateReportEntity) -> None:
        self._iam_repository.update_user_simultaneous_reports_generation(user.username, 1)
        report_id = self._reports_repository.create_user_report(
            username=user.username,
            report_name=generation_entity.name,
            report_type=generation_entity.report_type,
            processing_status=ReportProcessingResult.NEW,
        )

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

    def get_reports_preview(
        self,
        username: str,
        fetch_settings: ReportsFetchSettings | None = None,
    ) -> PaginatedDataEntity[ReportIdentificationEntity]:
        data: ReportIdentitiesQueryResult = self._reports_repository.get_user_reports(
            username,
            fetch_settings=fetch_settings,
        )

        self._logger.info(
            f"[ManagingReportsService] User {username} has totally: {data.total_reports} reports. "
            f"Has fetched {len(data.reports)} for page #{fetch_settings.page}."
        )

        return PaginatedDataEntity(
            data=data.reports,
            total_pages=math.ceil(data.total_reports / ITEMS_PER_PAGE),
            page=fetch_settings.page if fetch_settings else 0,
        )

    def set_report_name(self, username: str, name: str, report_id: int) -> ReportIdentificationEntity:
        self._logger.info(
            f"[ManagingReportsService] "
            f"Updating report `{report_id}` with new name: `{name}`"
        )

        new_report = self._reports_repository.update_report_name(
            report_id=report_id,
            username=username,
            name=name,
        )

        return ReportIdentificationEntity(
            report_id=new_report.report_id,
            name=new_report.name,
            report_type=new_report.report_type,
            generation_date=new_report.generation_date,
            processing_status=new_report.processing_status,
        )

    def get_detailed_report(
        self,
        username: str,
        report_id: int,
    ) -> BaseReport | StatisticalReport | WordCloudReport:
        return self._reports_repository.get_report(report_id, username=username)

    def delete_report(self, username: str, report_id: int) -> None:
        self._reports_repository.delete_report(report_id=report_id, username=username)
