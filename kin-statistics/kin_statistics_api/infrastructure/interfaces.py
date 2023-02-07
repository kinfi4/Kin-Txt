from abc import ABC, abstractmethod

from kin_statistics_api.domain.entities.report import (
    BaseReport,
    ReportIdentificationEntity,
    WordCloudReport,
    StatisticalReport,
)
from kin_statistics_api.constants import ReportProcessingResult


class IReportRepository(ABC):
    @abstractmethod
    def save_user_report(self, report: BaseReport) -> None:
        pass

    @abstractmethod
    def update_report_status(self, report_id: int, status: ReportProcessingResult) -> None:
        pass

    @abstractmethod
    def get_report(self, report_id: int) -> StatisticalReport | WordCloudReport:
        pass

    @abstractmethod
    def get_report_names(self, report_ids: list[int]) -> list[ReportIdentificationEntity]:
        pass

    @abstractmethod
    def update_report_name(self, report_id: int, report_name: str) -> ReportIdentificationEntity:
        pass

    @abstractmethod
    def delete_report(self, report_id: int) -> None:
        pass
