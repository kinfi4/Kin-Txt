import os
import logging
from typing import cast

from celery import Task

from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.domain.entities import (
    ModelValidationEntity,
    CreateModelEntity,
    UpdateModelEntity,
    ModelEntity,
)
from kin_reports_generation.exceptions import UnsupportedModelTypeError
from kin_reports_generation.infrastructure.repositories import ModelRepository


class ModelService:
    def __init__(
        self,
        models_storing_path: str,
        models_repository: ModelRepository,
    ) -> None:
        self._models_storing_path = models_storing_path
        self._models_repository = models_repository
        self._logger = logging.getLogger(__name__)

    def prepare_model_for_validation(self, username: str, model: CreateModelEntity) -> ModelEntity:
        """
            This method returns a model entity that needs to be validated.
        """

        model_to_save = self._prepare_model_for_saving(username, model)
        model_to_validate = self._models_repository.save_new_model(model_to_save)

        return model_to_validate

    def update_model(self, username: str, model_id: str, model: UpdateModelEntity) -> tuple[bool, ModelEntity | None]:
        """
            This method returns a tuple, with first elements indicating if model needs validation.
            While the second element is the model entity that needs to be validated or None if model doesn't need validation.
        """

        if model.models_has_changed:
            model_to_save = self._prepare_model_for_saving(username, model)
            model_to_validate = self._models_repository.update_model(model_id, username, model_to_save.dict())

            return True, model_to_validate

        update_dict = {
            "category_mapping": model.category_mapping,
            "name": model.name,
            "model_type": model.model_type,
        }

        self._models_repository.update_model(model_id, username, update_dict)

        return False, None

    def _prepare_model_for_saving(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        if model.model_type == ModelTypes.SKLEARN:
            return self._prepare_sk_learn_model_for_validation(username, model)

        raise UnsupportedModelTypeError(f"Model type {model.model_type} is not supported")

    def _prepare_sk_learn_model_for_validation(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        user_models_path = os.path.join(self._models_storing_path, username)

        if not os.path.exists(user_models_path):
            os.makedirs(user_models_path)

        model_file_path = os.path.join(user_models_path, model.name)
        tokenizer_file_path = os.path.join(user_models_path, f"tokenizer_{model.name}")
        with open(model_file_path, "wb") as file:
            file.write(model.model_data.file.read())
        with open(tokenizer_file_path, "wb") as file:
            file.write(model.tokenizer_data.file.read())

        return ModelValidationEntity(
            name=model.name,
            model_type=model.model_type,
            owner_username=username,
            model_path=model_file_path,
            tokenizer_path=tokenizer_file_path,
            category_mapping=model.category_mapping,
        )
