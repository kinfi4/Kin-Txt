from typing import TypeAlias

from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.domain.entities import CreateModelEntity
from kin_reports_generation.domain.services.model.validation.sklearn_validator import SkLearnModelValidator
from kin_reports_generation.exceptions import BaseValidationError

ValidationResult: TypeAlias = tuple[bool, str | None]


class ModelValidationService:
    _MODEL_TYPE_VALIDATOR_MAPPING = {
        ModelTypes.SKLEARN: SkLearnModelValidator,
    }

    def validate_model(self, create_model_entity: CreateModelEntity) -> ValidationResult:
        validator = self._MODEL_TYPE_VALIDATOR_MAPPING[create_model_entity.model_type]()

        try:
            validator.validate_model(create_model_entity)
        except BaseValidationError as error:
            return False, str(error)

        return True, None
