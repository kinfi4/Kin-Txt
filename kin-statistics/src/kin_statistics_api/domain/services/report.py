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
from kin_statistics_api.exceptions import ReportAccessForbidden
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
        self._iam_repository.update_user_simultaneous_reports_generation(username, -1)

        if not self._reports_repository.report_exists(report.report_id):
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

    def get_user_reports_names(
        self,
        username: str,
        fetch_settings: ReportsFetchSettings | None = None,
    ) -> PaginatedDataEntity[ReportIdentificationEntity]:
        query_result: ReportIdentitiesQueryResult = self._reports_repository.get_user_reports(
            username,
            fetch_settings=fetch_settings,
        )

        print(query_result)

        self._logger.info(f"[ManagingReportsService] got reports {query_result.count} identities for user: {username}")

        return PaginatedDataEntity(
            data=query_result.reports,
            total_pages=math.ceil(query_result.count / ITEMS_PER_PAGE),
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

    def get_user_detailed_report(self, username: str, report_id: int) -> BaseReport | StatisticalReport | WordCloudReport:
        # TODO: We can remove this check and implement filtering in the repository.
        # TODO: This way we can avoid fetching all reports and then filtering them

        self._check_user_access(username, report_ids=[report_id])

        return self._reports_repository.get_report(report_id)

    def delete_report(self, username: str, report_id: int) -> None:
        self._check_user_access(username, [report_id])

        self._reports_repository.delete_report(report_id=report_id)

    def _check_user_access(self, username: str, report_ids: list[int]) -> None:
        user_reports = self._iam_repository.get_user_report_ids(username=username)

        if not all([report_id in user_reports for report_id in report_ids]):
            raise ReportAccessForbidden("You do not have permission for this report!")
