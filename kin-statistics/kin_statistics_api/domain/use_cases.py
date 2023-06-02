from dependency_injector.wiring import inject, Provider
from dependency_injector.providers import Singleton

from kin_statistics_api.domain.services import CsvFileGenerator, JsonFileGenerator, IReportFileGenerator
from kin_statistics_api.exceptions import ReportDataNotFound
from kin_statistics_api.containers import Container


@inject
def file_generator_user_case(
    file_type: str,
    json_file_generator: Singleton[JsonFileGenerator] = Provider[Container.services.json_data_generator],
    csv_file_generator: Singleton[CsvFileGenerator] = Provider[Container.services.csv_data_generator],
) -> IReportFileGenerator:
    if file_type == 'json':
        return json_file_generator()
    elif file_type == 'csv':
        return csv_file_generator()

    raise ReportDataNotFound()
