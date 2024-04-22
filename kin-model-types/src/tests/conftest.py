import pytest
from fastapi import FastAPI

from kin_model_types.containers import Container
from kin_model_types.app import create_app
from kin_model_types.domain.services import ModelService


@pytest.fixture(scope="function")
def application() -> FastAPI:
    from kin_model_types.containers import DatabaseResource
    DatabaseResource._make_reflection = lambda a, b: None  # need that for unit tests to run

    return create_app()


@pytest.fixture(scope="function")
def container(application: FastAPI) -> Container:
    return application.container  # type: ignore


@pytest.fixture
def models_service(container: Container) -> ModelService:
    return container.domain_services.models_service()
