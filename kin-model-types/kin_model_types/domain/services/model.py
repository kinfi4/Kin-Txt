import os
import logging

from kin_model_types.events.events import ModelValidationRequestOccurred
from kin_news_core.messaging import AbstractEventProducer

from kin_model_types.constants import ModelTypes
from kin_model_types.domain.entities import (
    ModelValidationEntity,
    CreateModelEntity,
    UpdateModelEntity,
)
from kin_model_types.exceptions import UnsupportedModelTypeError
from kin_model_types.infrastructure.repositories import ModelRepository
from kin_model_types.constants import REPORTS_BUILDER_EXCHANGE


class ModelService:
    def __init__(
        self,
        models_storing_path: str,
        models_repository: ModelRepository,
        events_publisher: AbstractEventProducer,
    ) -> None:
        self._models_storing_path = models_storing_path
        self._models_repository = models_repository
        self._events_publisher = events_publisher

        self._logger = logging.getLogger(__name__)

    def validate_model(self, username: str, model: CreateModelEntity) -> None:
        """
            This method returns a model entity that needs to be validated.
        """

        model_to_save = self._prepare_model_for_saving(username, model)
        model_to_validate = self._models_repository.save_new_model(model_to_save)

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )

    def update_model(self, username: str, model_code: str, model: UpdateModelEntity) -> None:
        """
            This method returns a tuple, with first elements indicating if model needs validation.
            While the second element is the model entity that needs to be validated or None if model doesn't need validation.
        """

        old_model = self._models_repository.get_model(model_code, username)

        if model.models_has_changed:
            model_to_save = self._prepare_model_for_saving(username, model)

            if not model_to_save.model_path:
                model_to_save.model_path = old_model.model_path
            if not model_to_save.tokenizer_path:
                model_to_save.tokenizer_path = old_model.tokenizer_path

            model_to_validate = self._models_repository.update_model(model_code, username, model_to_save.dict())

            self._events_publisher.publish(
                REPORTS_BUILDER_EXCHANGE,
                [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
            )

            return None

        update_dict = {
            "category_mapping": model.category_mapping,
            "name": model.name,
            "model_type": model.model_type,
        }

        self._models_repository.update_model(model_code, username, update_dict)

    def _prepare_model_for_saving(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        if model.model_type == ModelTypes.SKLEARN:
            return self._prepare_model_validation_from_model_binaries(username, model)
        if model.model_type == ModelTypes.KERAS:
            return self._prepare_model_validation_from_model_binaries(username, model)

        raise UnsupportedModelTypeError(f"Model type {model.model_type} is not supported")

    def _prepare_model_validation_from_model_binaries(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        user_models_path = os.path.join(self._models_storing_path, username)

        if not os.path.exists(user_models_path):
            os.makedirs(user_models_path)

        if model.model_data is not None:
            model_file_path = os.path.join(user_models_path, model.code)
            with open(model_file_path, "wb") as file:
                file.write(model.model_data.file.read())
        else:
            model_file_path = ""

        if model.tokenizer_data is not None:
            tokenizer_file_path = os.path.join(user_models_path, f"tokenizer_{model.code}")
            with open(tokenizer_file_path, "wb") as file:
                file.write(model.tokenizer_data.file.read())
        else:
            tokenizer_file_path = ""

        return ModelValidationEntity(
            name=model.name,
            code=model.code,
            model_type=model.model_type,
            owner_username=username,
            model_path=model_file_path,
            tokenizer_path=tokenizer_file_path,
            category_mapping=model.category_mapping,
        )
