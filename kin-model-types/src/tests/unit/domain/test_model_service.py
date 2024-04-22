from unittest import mock

import pytest

from kin_model_types.domain.services import ModelService
from kin_txt_core.reports_building.constants import ModelTypes

from kin_model_types.domain.entities import CreateModelEntity, UpdateModelEntity, CustomModelRegistrationEntity, \
    ModelEntity
from kin_model_types.exceptions import ImpossibleToUpdateCustomModelException


class TestModelService:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, models_service: ModelService, mock_model_repository: mock.MagicMock) -> None:
        self.models_service = models_service
        self.mock_model_repository = mock_model_repository

    def test_validate_model(self) -> None:
        username = "test_user"
        model = CreateModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.BUILTIN,
            category_mapping={},
            preprocessing_config={},
        )

        self.mock_model_repository.save_new_model.return_value = ModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.BUILTIN,
            category_mapping={},
            preprocessing_config={},
            owner_username="test-username",
            model_status="Validated",
        )

        self.models_service.validate_model(username, model)

        self.mock_model_repository.save_new_model.assert_called_once_with(username, model)

    def test_update_model(self) -> None:
        username = "test_user"
        model_code = "test_code"
        model = UpdateModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.KERAS,
            category_mapping={},
            preprocessing_config={},
        )

        self.mock_model_repository.get_model.return_value = model
        self.mock_model_repository.update_model.return_value = ModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.KERAS,
            category_mapping={},
            preprocessing_config={},
            owner_username="test-username",
            model_status="Validated",
        )

        self.models_service.update_model(username, model_code, model)

        self.mock_model_repository.update_model.assert_called_once_with(model_code, username, model)

    def test_update_model_builtin_exception(self):
        username = "test_user"
        model_code = "test_code"
        model = UpdateModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.BUILTIN,
            category_mapping={},
            preprocessing_config={},
        )

        self.mock_model_repository.get_model.return_value = model

        with pytest.raises(ImpossibleToUpdateCustomModelException):
            self.models_service.update_model(username, model_code, model)

    def test_delete_model(self):
        username = "test_user"
        model_code = "test_code"

        self.models_service.delete_model(username, model_code)

        self.mock_model_repository.delete_model.assert_called_once_with(model_code, username)

    def test_register_custom_model(self):
        model_entity = CustomModelRegistrationEntity(
            code="test_code",
            name="test_name",
            owner_username="test_user",
            category_mapping={},
            preprocessing_config={},
            validation_needed=True,
        )
        self.mock_model_repository.save_new_model.return_value = ModelEntity(
            code="test_code",
            name="test_name",
            model_type=ModelTypes.BUILTIN,
            category_mapping={},
            preprocessing_config={},
            owner_username="test-username",
            model_status="Validated",
        )

        self.models_service.register_custom_model(model_entity)

        self.mock_model_repository.save_new_model.assert_called_once()

    def test_get_model(self):
        username = "test_user"
        model_code = "test_code"

        self.models_service.get_model(username, model_code)

        self.mock_model_repository.get_model.assert_called_once_with(model_code, username)
