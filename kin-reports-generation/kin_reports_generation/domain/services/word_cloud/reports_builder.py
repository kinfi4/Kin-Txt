from datetime import datetime
from typing import Optional
from typing_extensions import Self

from kin_reports_generation.domain.entities import WordCloudReport
from kin_reports_generation.constants import (
    MessageCategories,
    ReportProcessingResult,
    ReportTypes,
    SentimentTypes,
)


class WordCloudReportBuilder:
    def __init__(self, report_id: int) -> None:
        self._report_name = ""
        self._report_id = report_id
        self._total_words_count = 0
        self._report_type = ReportTypes.WORD_CLOUD
        self._status = ReportProcessingResult.READY
        self._failed_reason: Optional[str] = None
        self._report_generation_date = datetime.now()

        self._posts_categories = []

        self._data_by_channel_by_category: Optional[dict] = None
        self._data_by_channel: Optional[dict] = None
        self._data_by_category: Optional[dict] = None
        self._total_words_frequency: Optional[list[tuple[str, int]]] = None

    @classmethod
    def from_report_id(cls, report_id: int) -> Self:
        return cls(report_id=report_id)

    def set_posts_categories(self, posts_categories: list[str]) -> Self:
        self._posts_categories = posts_categories
        return self

    def set_report_name(self, name: str) -> Self:
        self._report_name = name
        return self

    def set_status(self, result_status: ReportProcessingResult) -> Self:
        self._status = result_status
        return self

    def set_failed_reason(self, reason: str) -> Self:
        self._failed_reason = reason
        return self

    def set_total_words_count(self, total_words: int) -> Self:
        self._total_words_count = total_words
        return self

    def set_data_by_channel_by_category(self, data: dict[str, dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]]) -> Self:
        self._data_by_channel_by_category = data
        return self

    def set_data_by_channel(self, data: dict[str, list[tuple[str, int]]]) -> Self:
        self._data_by_channel = data
        return self

    def set_data_by_category(self, data: dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]) -> Self:
        self._data_by_category = data
        return self

    def set_total_words_frequency(self, data: list[tuple[str, int]]) -> Self:
        self._total_words_frequency = data
        return self

    def build(self) -> WordCloudReport:
        return WordCloudReport(
            report_id=self._report_id,
            report_type=self._report_type,
            name=self._report_name,
            generation_date=self._report_generation_date,
            processing_status=self._status,
            report_failed_reason=self._failed_reason,
            total_words=self._total_words_count,
            data_by_category=self._data_by_category,
            data_by_channel=self._data_by_channel,
            data_by_channel_by_category=self._data_by_channel_by_category,
            total_words_frequency=self._total_words_frequency,
            posts_categories=self._posts_categories,
        )
