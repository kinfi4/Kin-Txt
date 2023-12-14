import logging

from kin_model_types.events.events import ModelValidationRequestOccurred, ModelDeleted
from kin_txt_core.messaging import AbstractEventProducer

from kin_model_types.constants import ModelTypes, GENERALE_EXCHANGE
from kin_model_types.domain.entities import (
    CreateModelEntity,
    UpdateModelEntity,
    CustomModelRegistrationEntity,
)
from kin_model_types.exceptions import ImpossibleToUpdateCustomModelException
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
        model_to_validate = self._models_repository.save_new_model(username, model)

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )

    def update_model(self, username: str, model_code: str, model: UpdateModelEntity) -> None:
        current_model = self._models_repository.get_model(model_code, username)

        if current_model.model_type == ModelTypes.CUSTOM:
            raise ImpossibleToUpdateCustomModelException(f"Impossible to update custom model {model_code}")

        model_to_validate = self._models_repository.update_model(model_code, username, model.dict(exclude_none=True))

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )

    def delete_model(self, username: str, model_code: str) -> None:
        self._logger.info(f"[ModelService] Deleting model {model_code} for user {username}")
        self._models_repository.delete_model(model_code, username)

        self._events_publisher.publish(
            GENERALE_EXCHANGE,
            [ModelDeleted(code=model_code, username=username)],
        )

    def register_custom_model(self, model_entity: CustomModelRegistrationEntity) -> None:
        self._logger.info(f"[ModelService] Registering custom model {model_entity.code} for user {model_entity.owner_username}")

        model_to_save = CreateModelEntity(
            code=model_entity.code,
            name=model_entity.name,
            model_type=ModelTypes.CUSTOM,
            category_mapping=model_entity.category_mapping,
        )

        model_to_validate = self._models_repository.save_new_model(model_entity.owner_username, model_to_save)

        self._events_publisher.publish(
            REPORTS_BUILDER_EXCHANGE,
            [ModelValidationRequestOccurred.parse_obj(model_to_validate.dict())],
        )
