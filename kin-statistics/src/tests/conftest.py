import pytest

from fastapi import FastAPI
from dependency_injector.providers import Container

from kin_statistics_api.app import create_app
from kin_statistics_api.domain.entities import GenerateReportEntity


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
        "templateId": "id-id-id-id",
        "startDate": "01/01/2022",
        "endDate": "01/02/2022",
        "modelType": "Sklearn Model",
        "channels": ["channel1", "channel2"],
    }

    return data, GenerateReportEntity(**data)
