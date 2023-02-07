from kin_news_core.messaging.dtos.event import BasicEvent

from kin_reports_generation.domain.entities import StatisticalReport, WordCloudReport, GenerateReportEntity, BaseReport


class GenerateReportRequestOccurred(BasicEvent, GenerateReportEntity):
    username: str


class ReportProcessingStarted(BasicEvent):
    report_id: int


class ReportProcessingFailed(BasicEvent, BaseReport):
    username: str


class WordCloudReportProcessingFinished(BasicEvent, WordCloudReport):
    username: str


class StatisticalReportProcessingFinished(BasicEvent, StatisticalReport):
    username: str
