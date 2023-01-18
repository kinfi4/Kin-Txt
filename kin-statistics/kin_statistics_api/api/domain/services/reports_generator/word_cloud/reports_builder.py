from datetime import datetime
from typing import Optional

from api.domain.entities import WordCloudReport
from config.constants import (
    MessageCategories,
    ReportProcessingResult,
    ReportTypes,
    SentimentTypes,
)


class WordCloudReportBuilder:
    def __init__(self, report_id: int) -> None:
        self._report_name = self._default_report_name_generator()
        self._report_id = report_id
        self._total_words_count = 0
        self._report_type = ReportTypes.WORD_CLOUD
        self._status = ReportProcessingResult.READY
        self._failed_reason: Optional[str] = None

        self._data_by_channel_by_category: Optional[dict] = None
        self._data_by_channel: Optional[dict] = None
        self._data_by_category: Optional[dict] = None
        self._total_words_frequency: Optional[list[tuple[str, int]]] = None

    @classmethod
    def from_report_id(cls, report_id: int) -> "WordCloudReportBuilder":
        return cls(report_id=report_id)

    def set_report_name(self, name: str) -> "WordCloudReportBuilder":
        self._report_name = name
        return self

    def set_status(self, result_status: ReportProcessingResult) -> "WordCloudReportBuilder":
        self._status = result_status
        return self

    def set_failed_reason(self, reason: str) -> "WordCloudReportBuilder":
        self._failed_reason = reason
        return self

    def set_total_words_count(self, total_words: int) -> "WordCloudReportBuilder":
        self._total_words_count = total_words
        return self

    def set_data_by_channel_by_category(self, data: dict[str, dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]]) -> "WordCloudReportBuilder":
        self._data_by_channel_by_category = data
        return self

    def set_data_by_channel(self, data: dict[str, list[tuple[str, int]]]) -> "WordCloudReportBuilder":
        self._data_by_channel = data
        return self

    def set_data_by_category(self, data: dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]) -> "WordCloudReportBuilder":
        self._data_by_category = data
        return self

    def set_total_words_frequency(self, data: list[tuple[str, int]]) -> "WordCloudReportBuilder":
        self._total_words_frequency = data
        return self

    def build(self) -> WordCloudReport:
        return WordCloudReport(
            report_id=self._report_id,
            report_type=self._report_type,
            name=self._report_name,
            processing_status=self._status,
            report_failed_reason=self._failed_reason,
            total_words=self._total_words_count,
            data_by_category=self._data_by_category,
            data_by_channel=self._data_by_channel,
            data_by_channel_by_category=self._data_by_channel_by_category,
            total_words_frequency=self._total_words_frequency,
        )

    @staticmethod
    def _default_report_name_generator() -> str:
        return f'Word Cloud: {datetime.now().strftime("%b %d, %Y %H:%M:%S")}'
