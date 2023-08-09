from typing_extensions import Self
from datetime import datetime

from kin_news_core.types.reports import RawContentTypes, VisualizationDiagramTypes
from kin_reports_generation.domain.entities import StatisticalReport
from kin_reports_generation.constants import (
    ReportProcessingResult,
    ReportTypes,
)
from kin_reports_generation.domain.entities.reports import DataByCategory, DataByDateChannelCategory


class ReportsBuilder:
    def __init__(
        self,
        report_id: int,
    ) -> None:
        self._report_id = report_id
        self._visualization_diagrams_list = None
        self._posts_categories = None

        self._report_name = ""

        self._total_messages_count = 0
        self._status = ReportProcessingResult.READY
        self._failed_reason: str | None = None
        self._report_type = ReportTypes.STATISTICAL
        self._report_generation_date = datetime.now()

        self._report_data: dict[RawContentTypes, DataByCategory | DataByDateChannelCategory] = {}

    @classmethod
    def from_report_id(cls, report_id: int) -> Self:
        return cls(report_id=report_id)

    def set_posts_categories(self, posts_categories: list[str]) -> Self:
        self._posts_categories = posts_categories
        return self

    def set_visualization_diagrams_list(self, visualization_diagrams_list: list[VisualizationDiagramTypes]) -> Self:
        self._visualization_diagrams_list = visualization_diagrams_list
        return self

    def set_report_name(self, name: str) -> Self:
        self._report_name = name
        return self

    def set_total_messages_count(self, total_messages: int) -> Self:
        self._total_messages_count = total_messages
        return self

    def set_data(self, data: dict[RawContentTypes, DataByCategory | DataByDateChannelCategory]) -> Self:
        self._report_data = data
        return self

    def set_status(self, result_status: ReportProcessingResult) -> Self:
        self._status = result_status
        return self

    def set_failed_reason(self, reason: str) -> Self:
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
            visualization_diagrams_list=self._visualization_diagrams_list,
            data=self._report_data,
        )
