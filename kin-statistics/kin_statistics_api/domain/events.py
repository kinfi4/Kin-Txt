from kin_statistics_api.domain.entities import (
    WordCloudReport,
    StatisticalReport,
    BaseReport,
    GenerateReportEntity,
)
from kin_news_core.messaging import BasicEvent


class GenerateReportRequestOccurred(BasicEvent, GenerateReportEntity):
    report_id: int
    username: str


class ReportProcessingStarted(BasicEvent):
    report_id: int


class ReportProcessingFailed(BasicEvent, BaseReport):
    username: str


class WordCloudReportProcessingFinished(BasicEvent, WordCloudReport):
    username: str


class StatisticalReportProcessingFinished(BasicEvent, StatisticalReport):
    username: str

