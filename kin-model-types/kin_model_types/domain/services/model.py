import os
import logging

from kin_model_types.events.events import ModelValidationRequestOccurred, ModelDeleted
from kin_news_core.messaging import AbstractEventProducer

from kin_model_types.constants import ModelTypes, GENERALE_EXCHANGE
from kin_model_types.domain.entities import (
    ModelValidationEntity,
    CreateModelEntity,
    UpdateModelEntity, CustomModelRegistrationEntity,
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
        model_to_save = self._prepare_model_for_saving(username, model)
        model_to_validate = self._models_repository.save_new_model(model_to_save)

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )

    def update_model(self, username: str, model_code: str, model: UpdateModelEntity) -> None:
        if model.models_has_changed:
            model_to_save = self._prepare_model_for_saving(username, model)

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

    def delete_model(self, username: str, model_code: str) -> None:
        self._logger.info(f"[ModelService] Deleting model {model_code} for user {username}")
        self._models_repository.delete_model(model_code, username)

        self._events_publisher.publish(
            GENERALE_EXCHANGE,
            [ModelDeleted(code=model_code, username=username)],
        )

    def register_custom_model(self, model_entity: CustomModelRegistrationEntity) -> None:
        self._logger.info(f"[ModelService] Registering custom model {model_entity.code} for user {model_entity.owner_username}")

        model_to_save = ModelValidationEntity(
            code=model_entity.code,
            name=model_entity.name,
            model_type=ModelTypes.CUSTOM,
            category_mapping=model_entity.category_mapping,
            owner_username=model_entity.owner_username,
        )

        model_to_validate = self._models_repository.save_new_model(model_to_save)

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )

    def _prepare_model_for_saving(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        model.save_model_binaries(self._models_storing_path, username)

        return ModelValidationEntity(
            code=model.code,
            name=model.name,
            model_type=model.model_type,
            category_mapping=model.category_mapping,
            owner_username=username,
        )
