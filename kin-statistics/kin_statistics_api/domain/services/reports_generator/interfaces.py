import logging
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

from kin_statistics_api.domain.entities import BaseReport, GenerateReportEntity, StatisticalReport, WordCloudReport
from kin_statistics_api.domain.services.reports_generator.predictor.interfaces import IPredictor
from kin_statistics_api.domain.services.reports_generator.statistical_report.reports_builder import (
    ReportsBuilder,
)
from kin_statistics_api.domain.services.reports_generator.word_cloud.reports_builder import (
    WordCloudReportBuilder,
)
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.infrastructure.repositories import ReportsAccessManagementRepository
from kin_statistics_api.constants import ReportProcessingResult
from kin_news_core.telegram import IDataGetterProxy


class IGeneratingReportsService(ABC):
    reports_builder: WordCloudReportBuilder | ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        reports_repository: IReportRepository,
        report_access_repository: ReportsAccessManagementRepository,
        predictor: IPredictor,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._telegram = telegram_client
        self._reports_repository = reports_repository
        self._access_repository = report_access_repository
        self._predictor = predictor

    def generate_report(self, generate_report_entity: GenerateReportEntity, username: str) -> BaseReport:
        self._logger.info(f'[{self.__class__.__name__}] Starting generating report for user: {username}')

        self._access_repository.set_user_began_report_generation(username)
        report_id = self._access_repository.create_new_user_report(username)

        empty_report = self._build_empty_report(report_id)
        self._reports_repository.save_user_report(empty_report)

        try:
            report_entity = self._build_report_entity(report_id, generate_report_entity)

            self._reports_repository.save_user_report(report_entity)

            return report_entity
        except Exception as error:
            self._logger.error(
                f'[{self.__class__.__name__}]'
                f' {error.__class__.__name__} occurred during processing report for user: {username} with message: {str(error)}'
            )

            postponed_report = self._build_postponed_report(report_id, error)
            self._reports_repository.save_user_report(postponed_report)
        finally:
            self._access_repository.set_user_finished_report_generation(username)

    @abstractmethod
    def _build_report_entity(self, report_id: int, generate_report_entity: GenerateReportEntity):
        pass

    @staticmethod
    def _datetime_from_date(dt: date, end_of_day: bool = False) -> datetime:
        return datetime(year=dt.year, month=dt.month, day=dt.day) + timedelta(days=int(end_of_day))

    @classmethod
    def _build_empty_report(cls, report_id: int) -> StatisticalReport | WordCloudReport:
        return (
            cls.reports_builder.from_report_id(report_id)
            .set_status(ReportProcessingResult.PROCESSING)
            .build()
        )

    @classmethod
    def _build_postponed_report(cls, report_id: int, error: Exception) -> StatisticalReport | WordCloudReport:
        return (
            cls.reports_builder.from_report_id(report_id)
            .set_status(ReportProcessingResult.POSTPONED)
            .set_failed_reason(str(error))
            .build()
        )
