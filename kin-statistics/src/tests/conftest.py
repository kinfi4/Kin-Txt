import pytest

from fastapi import FastAPI
from dependency_injector.providers import Container

from kin_statistics_api.app import create_app
from kin_statistics_api.domain.entities import GenerateReportEntity
from kin_statistics_api.domain.services import (
    ManagingReportsService,
    ReportDataSaver,
    JsonFileGenerator,
    CsvFileGenerator,
)


@pytest.fixture(scope="function")
def application() -> FastAPI:
    return create_app()


@pytest.fixture(scope="function")
def container(application: FastAPI) -> Container:
    return application.container  # type: ignore


@pytest.fixture(scope="function")
def generate_report_entity() -> tuple[dict, GenerateReportEntity]:
    data = {
        "name": "test_report",
        "reportType": "Statistical",
        "modelCode": "test_report",
        "templateId": 5,
        "startDate": "01/01/2022",
        "endDate": "01/02/2022",
        "modelType": "Sklearn Model",
        "channels": ["channel1", "channel2"],
    }

    return data, GenerateReportEntity(**data)


@pytest.fixture(scope="function")
def reports_service(container: Container) -> ManagingReportsService:
    return container.services.managing_reports_service()


@pytest.fixture(scope="function")
def reports_data_saver(container: Container) -> ReportDataSaver:
    return container.services.reports_data_saver()


@pytest.fixture(scope="function")
def json_file_generator(container: Container) -> JsonFileGenerator:
    return container.services.json_data_generator()


@pytest.fixture(scope="function")
def csv_file_generator(container: Container) -> CsvFileGenerator:
    return container.services.csv_data_generator()
