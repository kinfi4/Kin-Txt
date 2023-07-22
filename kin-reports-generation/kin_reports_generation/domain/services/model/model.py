import os
import logging

from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.domain.entities import ModelValidationEntity, CreateModelEntity
from kin_reports_generation.domain.services.model.validation import ModelValidationService
from kin_reports_generation.exceptions import BaseValidationError
from kin_reports_generation.infrastructure.repositories import ModelRepository


class ModelService:
    def __init__(
        self,
        models_storing_path: str,
        models_repository: ModelRepository,
        validation_service: ModelValidationService,
    ) -> None:
        self._validation_service = validation_service
        self._models_storing_path = models_storing_path
        self._models_repository = models_repository
        self._logger = logging.getLogger(__name__)

    def validate_and_save(self, username: str, model: ModelValidationEntity) -> None:
        create_model_entity = self._prepare_model_for_validation(username, model)
        validation_result, validation_message = self._validation_service.validate_model(create_model_entity)

        if not validation_result:
            self._logger.error(f"Model validation failed: {validation_message}")
            raise BaseValidationError(validation_message)

        self._models_repository.save_model(create_model_entity)

    def _prepare_model_for_validation(self, username: str, model: ModelValidationEntity) -> CreateModelEntity:
        if model.model_type == ModelTypes.SKLEARN:
            return self._prepare_sk_learn_model_for_validation(username, model)

    def _prepare_sk_learn_model_for_validation(self, username: str, model: ModelValidationEntity) -> CreateModelEntity:
        user_models_path = os.path.join(self._models_storing_path, username)

        if not os.path.exists(user_models_path):
            os.makedirs(user_models_path)

        model_file_path = os.path.join(user_models_path, model.name)
        tokenizer_file_path = os.path.join(user_models_path, f"tokenizer_{model.name}")
        with open(model_file_path, "wb") as file:
            file.write(model.model_data.file.read())
        with open(tokenizer_file_path, "wb") as file:
            file.write(model.tokenizer_data.file.read())

        return CreateModelEntity(
            name=model.name,
            model_type=model.model_type,
            owner_username=username,
            model_path=model_file_path,
            tokenizer_path=tokenizer_file_path,
            category_list=model.category_list,
        )
