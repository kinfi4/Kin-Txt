from abc import ABC, abstractmethod
from typing import IO

from kin_statistics_api.exceptions import ReportDataNotFound
from kin_statistics_api.infrastructure.repositories import IAMRepository
from kin_statistics_api.domain.entities import User


class IReportFileGenerator(ABC):
    def __init__(self, iam_repository: IAMRepository):
        self._iam_repository = iam_repository

    @abstractmethod
    def get_file(self, user: User, report_id: int) -> tuple[IO, str]:
        pass

    def _check_user_access(self, user: User, report_id: int) -> None:
        if report_id not in self._iam_repository.get_user_report_ids(user.username):
            raise ReportDataNotFound()
