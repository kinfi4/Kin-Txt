from unittest import mock

import pytest

from kin_statistics_api.containers import Container


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
    repository = container.repositories.iam_repository
    with repository.override(mock.MagicMock()):
        yield repository()

    repository.reset_override()


@pytest.fixture(scope="function", autouse=True)
def mock__events_producer(container: Container) -> mock.MagicMock:
    events_producer = container.messaging.producer
    with events_producer.override(mock.MagicMock()):
        yield events_producer()

    events_producer.reset_override()
