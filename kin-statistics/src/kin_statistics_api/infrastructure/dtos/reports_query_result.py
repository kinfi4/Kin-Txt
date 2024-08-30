from dataclasses import dataclass

from kin_statistics_api.domain.entities import ReportIdentificationEntity


@dataclass
class ReportIdentitiesQueryResult:
    reports: list[ReportIdentificationEntity]
    total_reports: int
