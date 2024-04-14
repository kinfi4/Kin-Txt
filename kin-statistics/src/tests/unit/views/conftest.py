from unittest import mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from kin_txt_core.auth import create_jwt_token


@pytest.fixture(scope="function")
def test_http_client__unauthorized(application: FastAPI) -> TestClient:
    yield TestClient(application)


@pytest.fixture(scope="function")
def username_with_access_token_headers(application: FastAPI) -> tuple[str, dict[str, str]]:
    username = "test-username"
    user_jwt_token = create_jwt_token(username)

    yield username, {"Authorization": f"Token {user_jwt_token}"}
