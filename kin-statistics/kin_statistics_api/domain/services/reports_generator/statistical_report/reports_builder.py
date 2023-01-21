from datetime import datetime
from typing import Optional

from api.domain.entities import StatisticalReport
from config.constants import (
    MessageCategories,
    ReportProcessingResult,
    ReportTypes,
    SentimentTypes,
)


class ReportsBuilder:
    def __init__(self, report_id: int) -> None:
        self._report_name = self._default_report_name_generator()
        self._report_id = report_id
        self._total_messages_count = 0
        self._status = ReportProcessingResult.READY
        self._failed_reason: Optional[str] = None
        self._report_type = ReportTypes.STATISTICAL

        self._messages_count_by_category = {category: 0 for category in MessageCategories}
        self._messages_count_by_sentiment_type = {sentiment_type: 0 for sentiment_type in SentimentTypes}
        self._messages_count_by_day_hour = {str(hour): 0 for hour in range(24)}
        self._messages_count_by_date: dict = {}
        self._messages_count_by_channel: dict = {}
        self._messages_count_by_date_by_category: dict = {}
        self._messages_count_by_channel_by_category: dict = {}
        self._messages_count_by_channel_by_sentiment_type: dict = {}
        self._messages_count_by_date_by_sentiment_type: dict = {}

    @classmethod
    def from_report_id(cls, report_id: int) -> "ReportsBuilder":
        return cls(report_id=report_id)

    def set_report_name(self, name: str) -> "ReportsBuilder":
        self._report_name = name
        return self

    def set_total_messages_count(self, total_messages: int) -> "ReportsBuilder":
        self._total_messages_count = total_messages
        return self

    def set_messages_count_by_channel(self, messages_by_channel: dict[str, int]) -> "ReportsBuilder":
        self._messages_count_by_channel = messages_by_channel
        return self

    def set_messages_count_by_date(self, messages_by_date: dict[str, int]) -> "ReportsBuilder":
        self._messages_count_by_date = messages_by_date
        return self

    def set_messages_count_by_date_by_category(self, messages_count: dict[str, dict[MessageCategories, int]]) -> "ReportsBuilder":
        self._messages_count_by_date_by_category = messages_count
        return self

    def set_messages_count_by_channel_by_category(self, messages_count: dict[str, dict[MessageCategories, int]]) -> "ReportsBuilder":
        self._messages_count_by_channel_by_category = messages_count
        return self

    def set_messages_count_by_sentiment_type(self, messages_count: dict[SentimentTypes, int]) -> "ReportsBuilder":
        self._messages_count_by_sentiment_type = messages_count
        return self

    def set_messages_count_by_channel_by_sentiment_type(self, messages_count: dict[str, dict[SentimentTypes, int]]) -> "ReportsBuilder":
        self._messages_count_by_channel_by_sentiment_type = messages_count
        return self

    def set_messages_count_by_date_by_sentiment_type(self, messages_count: dict[str, dict[SentimentTypes, int]]) -> "ReportsBuilder":
        self._messages_count_by_date_by_sentiment_type = messages_count
        return self

    def set_messages_count_by_day_hour(self, messages_by_hour: dict[str, int]) -> "ReportsBuilder":
        self._messages_count_by_day_hour = messages_by_hour
        return self

    def set_messages_count_by_category(self, messages_by_category: dict[MessageCategories, int]) -> "ReportsBuilder":
        self._messages_count_by_category = messages_by_category
        return self

    def set_status(self, result_status: ReportProcessingResult) -> "ReportsBuilder":
        self._status = result_status
        return self

    def set_failed_reason(self, reason: str) -> "ReportsBuilder":
        self._failed_reason = reason
        return self

    def build(self) -> StatisticalReport:
        return StatisticalReport(
            report_id=self._report_id,
            name=self._report_name,
            report_type=self._report_type,
            processing_status=self._status,
            report_failed_reason=self._failed_reason,
            total_messages_count=self._total_messages_count,
            messages_count_by_category=self._messages_count_by_category,
            messages_count_by_day_hour=self._messages_count_by_day_hour,
            messages_count_by_date=self._messages_count_by_date,
            messages_count_by_channel=self._messages_count_by_channel,
            messages_count_by_date_by_category=self._messages_count_by_date_by_category,
            messages_count_by_channel_by_category=self._messages_count_by_channel_by_category,
            messages_count_by_sentiment_type=self._messages_count_by_sentiment_type,
            messages_count_by_channel_by_sentiment_type=self._messages_count_by_channel_by_sentiment_type,
            messages_count_by_date_by_sentiment_type=self._messages_count_by_date_by_sentiment_type,
        )

    @staticmethod
    def _default_report_name_generator() -> str:
        return f'News Reports: {datetime.now().strftime("%b %d, %Y %H:%M:%S")}'
