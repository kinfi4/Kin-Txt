from unittest.mock import MagicMock

import bcrypt
from fastapi import status
from fastapi.testclient import TestClient

from kin_statistics_api.constants import API_ROUTE_PATH
from kin_statistics_api.domain.entities import UserLoginEntity, User
from kin_statistics_api.exceptions import UsernameAlreadyTakenError


class TestUserAccountsViews:
    def test_user_login__existing_user(
        self,
        test_http_client__unauthorized: TestClient,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username, password = "test", "test"
        mock__access_management_repository.get_user.return_value = UserLoginEntity(
            username=username,
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        )

        response = test_http_client__unauthorized.post(
            f"{API_ROUTE_PATH}/accounts/login",
            json={"username": username, "password": password},
        )

        assert response.status_code == status.HTTP_200_OK

    def test_user_login__non_existing_user(
        self,
        test_http_client__unauthorized: TestClient,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username, password = "test", "test"
        mock__access_management_repository.get_user.return_value = None

        response = test_http_client__unauthorized.post(
            f"{API_ROUTE_PATH}/accounts/login",
            json={"username": username, "password": password},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_registration__success(
        self,
        test_http_client__unauthorized: TestClient,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username, password1, password2 = "test", "test", "test"
        mock__access_management_repository.create_user.return_value = User(username=username)

        response = test_http_client__unauthorized.post(
            f"{API_ROUTE_PATH}/accounts/register",
            json={"username": username, "password": password1, "passwordRepeated": password2},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_registration__password_repeat_incorrect(
        self,
        test_http_client__unauthorized: TestClient,
    ) -> None:
        username, password1, password2 = "test", "test", "another-test"
        response = test_http_client__unauthorized.post(
            f"{API_ROUTE_PATH}/accounts/register",
            json={"username": username, "password": password1, "passwordRepeated": password2},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_user_registration__user_exists(
        self,
        test_http_client__unauthorized: TestClient,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username, password1, password2 = "test", "test", "test"
        mock__access_management_repository.create_user.side_effect = UsernameAlreadyTakenError()
        response = test_http_client__unauthorized.post(
            f"{API_ROUTE_PATH}/accounts/register",
            json={"username": username, "password": password1, "passwordRepeated": password2},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"errors": "User with specified username already exists"}

    def test_get_user(
        self,
        test_http_client__unauthorized: TestClient,
        username_with_access_token_headers: tuple[str, dict[str, str]],
    ) -> None:
        username, auth_headers = username_with_access_token_headers

        client = test_http_client__unauthorized
        response = client.get(f"{API_ROUTE_PATH}/accounts/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"username": username}
