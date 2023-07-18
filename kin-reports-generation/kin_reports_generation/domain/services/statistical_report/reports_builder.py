from datetime import datetime
from typing import Optional

from kin_reports_generation.domain.entities import StatisticalReport
from kin_reports_generation.constants import (
    ReportProcessingResult,
    ReportTypes,
    VisualizationDiagrams,
)
from kin_reports_generation.domain.entities.reports import DataByCategory, DataByDateChannelCategory


class ReportsBuilder:
    def __init__(self, report_id: int, set_of_diagrams_to_visualize: set[VisualizationDiagrams], posts_categories: list[str]) -> None:
        self._report_name = self._default_report_name_generator()
        self._report_id = report_id
        self._total_messages_count = 0
        self._status = ReportProcessingResult.READY
        self._failed_reason: Optional[str] = None
        self._report_type = ReportTypes.STATISTICAL
        self._report_generation_date = datetime.now()
        self._set_of_diagrams_to_visualize = set_of_diagrams_to_visualize
        self._posts_categories = posts_categories

        self._report_data: dict[VisualizationDiagrams, DataByCategory | DataByDateChannelCategory] = {}

    def set_report_name(self, name: str) -> "ReportsBuilder":
        self._report_name = name
        return self

    def set_total_messages_count(self, total_messages: int) -> "ReportsBuilder":
        self._total_messages_count = total_messages
        return self

    def set_data(self, data: dict[VisualizationDiagrams, DataByCategory | DataByDateChannelCategory]) -> "ReportsBuilder":
        self._report_data = data
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
            generation_date=self._report_generation_date,
            report_type=self._report_type,
            processing_status=self._status,
            report_failed_reason=self._failed_reason,
            posts_categories=self._posts_categories,
            total_messages_count=self._total_messages_count,
            set_of_diagrams_to_visualize=self._set_of_diagrams_to_visualize,
            data=self._report_data,
        )

    @staticmethod
    def _default_report_name_generator() -> str:
        return f'News Reports: {datetime.now().strftime("%b %d, %Y %H:%M:%S")}'
