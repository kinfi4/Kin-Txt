from abc import ABC, abstractmethod

from api.domain.entities import StatisticalReport
from api.domain.entities.report import (
    BaseReport,
    ReportIdentificationEntity,
    WordCloudReport,
)


class IReportRepository(ABC):
    @abstractmethod
    def save_user_report(self, report: BaseReport) -> None:
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
