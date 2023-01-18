from abc import ABC, abstractmethod
from typing import IO


class IReportFileGenerator(ABC):
    @abstractmethod
    def get_file(self, report_id: int) -> tuple[IO, str]:
        pass
