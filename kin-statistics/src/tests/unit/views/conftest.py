from unittest import mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dependency_injector.providers import Container

from kin_txt_core.auth import create_jwt_token


@pytest.fixture(scope="function")
def test_http_client__unauthorized(application: FastAPI) -> TestClient:
    yield TestClient(application)


@pytest.fixture(scope="function")
def username_with_access_token_headers(application: FastAPI) -> tuple[str, dict[str, str]]:
    username = "test-username"
    user_jwt_token = create_jwt_token(username)

    yield username, {"Authorization": f"Token {user_jwt_token}"}


@pytest.fixture(scope="function", autouse=True)
def mock__reports_repository(container: Container) -> mock.MagicMock:
    repository = container.repositories.reports_repository
    with repository.override(mock.MagicMock()):
        yield repository()

    repository.reset_override()


@pytest.fixture(scope="function", autouse=True)
def mock__templates_repository(container: Container) -> mock.MagicMock:
    repository = container.repositories.templates_repository
    with repository.override(mock.MagicMock()):
        yield repository()

    repository.reset_override()


@pytest.fixture(scope="function", autouse=True)
def mock__access_management_repository(container: Container) -> mock.MagicMock:
    repository = container.repositories.reports_access_management_repository
    with repository.override(mock.MagicMock()):
        yield repository()

    repository.reset_override()


@pytest.fixture(scope="function", autouse=True)
def mock__events_producer(container: Container) -> mock.MagicMock:
    events_producer = container.messaging.producer
    with events_producer.override(mock.MagicMock()):
        yield events_producer()

    events_producer.reset_override()
