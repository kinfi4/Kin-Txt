import logging
from typing import TypeAlias

from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.domain.services.model.validation.sklearn_validator import SkLearnModelValidator
from kin_reports_generation.exceptions import BaseValidationError
from kin_reports_generation.infrastructure.repositories import ModelRepository

ValidationResult: TypeAlias = tuple[bool, str | None]


class ModelValidationService:
    _MODEL_TYPE_VALIDATOR_MAPPING = {
        ModelTypes.SKLEARN: SkLearnModelValidator,
    }

    def __init__(self, model_repository: ModelRepository) -> None:
        self._model_repository = model_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def validate_model(self, model_entity: ModelEntity) -> ValidationResult:
        self._logger.info(f"[ModelValidationService] Validating model for user {model_entity.owner_username}...")

        validator_class = self._MODEL_TYPE_VALIDATOR_MAPPING[model_entity.model_type]
        validator = validator_class()

        try:
            validator.validate_model(model_entity)
        except BaseValidationError as error:
            return False, str(error)

        return True, None
