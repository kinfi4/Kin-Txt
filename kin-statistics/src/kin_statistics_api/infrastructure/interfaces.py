from abc import ABC, abstractmethod

from kin_txt_core.reports_building.constants import ReportTypes

from kin_statistics_api.domain.entities import ReportsFetchSettings
from kin_statistics_api.domain.entities.report import (
    BaseReport,
    ReportIdentificationEntity,
    WordCloudReport,
    StatisticalReport,
)
from kin_statistics_api.constants import ReportProcessingResult


class IReportRepository(ABC):
    @abstractmethod
    def get_user_reports(
        self,
        username: str,
        fetch_settings: ReportsFetchSettings | None,
    ) -> tuple[list[ReportIdentificationEntity], int]:
        pass

    @abstractmethod
    def save_finished_report(self, finished_report: WordCloudReport | StatisticalReport) -> None:
        pass

    @abstractmethod
    def create_user_report(
        self,
        username: str,
        report_name: str,
        report_type: ReportTypes,
        processing_status: ReportProcessingResult,
    ) -> int:
        """
        Must return report id
        """
        pass

    @abstractmethod
    def update_report_status(self, report_id: int, status: ReportProcessingResult) -> None:
        pass

    @abstractmethod
    def get_report(self, report_id: int) -> BaseReport | StatisticalReport | WordCloudReport:
        pass

    @abstractmethod
    def get_report_names(self, report_ids: list[int], apply_settings: ReportsFetchSettings | None = None) -> list[ReportIdentificationEntity]:
        pass

    @abstractmethod
    def update_report_name(self, report_id: int, report_name: str) -> ReportIdentificationEntity:
        pass

    @abstractmethod
    def delete_report(self, report_id: int) -> None:
        pass

    @abstractmethod
    def report_exists(self, report_id: int) -> bool:
        pass

    @abstractmethod
    def get_total_reports_count(self, filters: ReportsFetchSettings | None) -> int:
        pass
