from datetime import datetime

from dependency_injector.wiring import inject, Provide

from kin_statistics_api.domain.entities import (
    BaseReport,
    WordCloudReport,
    StatisticalReport,
)
from kin_statistics_api.domain.events import (
    ReportProcessingFailed,
    WordCloudReportProcessingFinished,
    StatisticalReportProcessingFinished,
    ReportProcessingStarted,
)
from kin_statistics_api.domain.services import ManagingReportsService
from kin_statistics_api.containers import Container
from kin_statistics_api.constants import ReportProcessingResult


@inject
def on_processing_started(
    event: ReportProcessingStarted,
    report_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
) -> None:
    report_service.update_report_status(event.report_id, ReportProcessingResult.PROCESSING)


@inject
def on_processing_failed(
    event: ReportProcessingFailed,
    report_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
) -> None:
    report = BaseReport(**event.dict(exclude={"username"}))
    report_service.report_processing_finished(event.username, report)


@inject
def on_processing_finished(
    event: WordCloudReportProcessingFinished | StatisticalReportProcessingFinished,
    report_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
) -> None:
    report = _get_report_from_event(event)
    report_service.report_processing_finished(event.username, report)


def _get_report_from_event(
    event: WordCloudReportProcessingFinished | StatisticalReportProcessingFinished
) -> WordCloudReport | StatisticalReport:
    if isinstance(event, WordCloudReportProcessingFinished):
        return WordCloudReport(**event.dict(exclude={"username"}))
    elif isinstance(event, StatisticalReportProcessingFinished):
        return StatisticalReport(**event.dict(exclude={"username"}))

    raise RuntimeError("Unknown event occurred for processing finished.")


def _generate_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")
