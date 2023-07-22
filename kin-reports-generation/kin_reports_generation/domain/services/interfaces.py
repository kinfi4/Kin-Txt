import logging
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

from kin_news_core.telegram import IDataGetterProxy
from kin_news_core.messaging import AbstractEventProducer

from kin_reports_generation.domain.entities import GenerateReportEntity, StatisticalReport, WordCloudReport
from kin_reports_generation.domain.events import (
    ReportProcessingStarted,
    WordCloudReportProcessingFinished,
    StatisticalReportProcessingFinished,
)
from kin_reports_generation.domain.services.predictor.news_category import NewsCategoryPredictor
from kin_reports_generation.domain.services.statistical_report.reports_builder import ReportsBuilder
from kin_reports_generation.domain.services.word_cloud.reports_builder import WordCloudReportBuilder
from kin_reports_generation.constants import ReportProcessingResult, REPORTS_STORING_EXCHANGE
from kin_reports_generation.infrastructure.repositories import ModelRepository


class IGeneratingReportsService(ABC):
    _REPORT_TYPE_TO_EVENT_MAPPING = {
        WordCloudReport: WordCloudReportProcessingFinished,
        StatisticalReport: StatisticalReportProcessingFinished,
    }

    reports_builder: WordCloudReportBuilder | ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        events_producer: AbstractEventProducer,
        models_repository: ModelRepository,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._telegram = telegram_client
        self._events_producer = events_producer
        self._models_repository = models_repository

    def generate_report(self, generate_report_entity: GenerateReportEntity, username: str) -> None:
        self._logger.info(f'[{self.__class__.__name__}] Starting generating report for user: {username}')
        self._publish_report_processing_started(generate_report_entity.report_id)

        try:
            predictor = self._initialize_predictor(generate_report_entity.model_id, username)

            report_entity = self._build_report_entity(generate_report_entity)
            self._publish_finished_report(username, report_entity)
        except Exception as error:
            self._logger.error(
                f'[{self.__class__.__name__}]'
                f' {error.__class__.__name__} occurred during processing report for user: {username} with message: {str(error)}'
            )

            error.with_traceback(error.__traceback__)

            postponed_report = self._build_postponed_report(generate_report_entity.report_id, error)
            self._publish_finished_report(username, postponed_report)

    @abstractmethod
    def _build_report_entity(self, generate_report_entity: GenerateReportEntity):
        pass

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

    def _datetime_from_date(self, dt: date, end_of_day: bool = False) -> datetime:
        return datetime(year=dt.year, month=dt.month, day=dt.day) + timedelta(days=int(end_of_day))

    def _initialize_predictor(self, model_id: str, username: str) -> NewsCategoryPredictor:
        model = self._models_repository.get_model(model_id, username)
        return NewsCategoryPredictor(model)

    def _publish_report_processing_started(self, report_id: int) -> None:
        event = ReportProcessingStarted(report_id=report_id)

        self._events_producer.publish(
            REPORTS_STORING_EXCHANGE,
            [event],
        )

    def _publish_finished_report(self, username: str, report: WordCloudReport | StatisticalReport) -> None:
        event_type = self._REPORT_TYPE_TO_EVENT_MAPPING[type(report)]
        event = event_type(**report.dict(), username=username)

        self._events_producer.publish(
            REPORTS_STORING_EXCHANGE,
            [event],
        )
