import csv
import io
import json
import os
from typing import IO, Optional

from django.conf import settings

from api.domain.services.interfaces import IReportFileGenerator
from api.exceptions import ReportDataNotFound


def file_generator_user_case(file_type: str) -> Optional[IReportFileGenerator]:
    if file_type == 'json':
        return JsonFileGenerator()
    elif file_type == 'csv':
        return CsvFileGenerator()

    raise ReportDataNotFound()


class JsonFileGenerator(IReportFileGenerator):
    def get_file(self, report_id: int) -> tuple[IO, str]:
        try:
            with open(os.path.join(settings.USER_REPORTS_FOLDER_PATH, f'{report_id}.csv')) as csv_file:
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
    def get_file(self, report_id: int) -> tuple[IO, str]:
        try:
            return open(os.path.join(settings.USER_REPORTS_FOLDER_PATH, f'{report_id}.csv')), f'report-{report_id}.csv'
        except FileNotFoundError:
            raise ReportDataNotFound()
