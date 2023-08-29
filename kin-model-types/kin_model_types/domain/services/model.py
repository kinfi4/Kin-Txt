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

    def _prepare_model_for_saving(self, username: str, model: CreateModelEntity) -> ModelValidationEntity:
        model.save_model_binaries(self._models_storing_path, username)

        return ModelValidationEntity(
            code=model.code,
            name=model.name,
            model_type=model.model_type,
            category_mapping=model.category_mapping,
            owner_username=username,
        )
