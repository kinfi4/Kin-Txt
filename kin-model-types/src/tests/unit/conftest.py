from unittest import mock

import pytest
from pytest_mock import MockFixture

from kin_model_types.containers import Container


@pytest.fixture(autouse=True)
def mock_model_repository(container: Container, mocker: MockFixture) -> mock.MagicMock:
    repository = container.repositories.model_repository
    with repository.override(mocker.MagicMock(repository.cls)):
        yield repository()

    repository.reset_override()


@pytest.fixture(autouse=True)
def mock_vis_templates_repository(container: Container, mocker: MockFixture) -> mock.MagicMock:
    repository = container.repositories.visualization_template_repository
    with repository.override(mocker.MagicMock(repository.cls)):
        yield repository()

    repository.reset_override()


@pytest.fixture(autouse=True)
def mock_events_publisher(container: Container, mocker: MockFixture) -> mock.MagicMock:
    events_publisher = container.messaging.producer
    with events_publisher.override(mocker.MagicMock(events_publisher.cls)):
        yield events_publisher()

    events_publisher.reset_override()
