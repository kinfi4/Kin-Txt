import csv
import io
import json
import os
from typing import IO, BinaryIO

from kin_statistics_api.domain.entities import User
from kin_statistics_api.domain.services.interfaces import IReportFileGenerator
from kin_statistics_api.exceptions import ReportDataNotFound
from kin_statistics_api.settings import Settings


class JsonFileGenerator(IReportFileGenerator):
    def get_file(self, user: User, report_id: int) -> tuple[IO, str]:
        self._check_user_access(user, report_id)

        try:
            with open(os.path.join(Settings().reports_folder_path, f'{report_id}.csv')) as csv_file:
                return self._transform_csv_to_json(csv_file), f'report-{report_id}.json'
        except FileNotFoundError:
            raise ReportDataNotFound()

    @staticmethod
    def _transform_csv_to_json(csv_file: IO) -> IO:
        csv_reader = csv.DictReader(csv_file)

        data = [dict_row for dict_row in csv_reader]
        data_string = json.dumps(data, ensure_ascii=False)

        return io.StringIO(data_string)


class CsvFileGenerator(IReportFileGenerator):
    def get_file(self, user: User, report_id: int) -> tuple[IO, str]:
        self._check_user_access(user, report_id)

        try:
            return open(os.path.join(Settings().reports_folder_path, f'{report_id}.csv')), f'report-{report_id}.csv'
        except FileNotFoundError:
            raise ReportDataNotFound()


class ReportDataSaver:
    SUPPORTED_FILE_TYPES = ('csv', 'json')

    def __init__(self, reports_folder_path: str) -> None:
        self._reports_folder_path = reports_folder_path

    def save_report_data(self, report_id: int, file_type: str, data_file: BinaryIO) -> None:
        if file_type not in self.SUPPORTED_FILE_TYPES:
            raise ValueError(f'[ReportDataSaver] Invalid file type for report={report_id} data.')

        with open(os.path.join(self._reports_folder_path, f'{report_id}.{file_type}'), 'wb') as file:
            file.write(data_file.read())
