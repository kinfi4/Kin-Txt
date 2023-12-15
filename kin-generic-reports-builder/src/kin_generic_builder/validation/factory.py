import logging
from typing import Type

from kin_txt_core.reports_building.constants import ModelTypes
from kin_txt_core.reports_building.settings import Settings as DefaultSettings
from kin_txt_core.reports_building.domain.entities import ModelEntity
from kin_txt_core.reports_building.domain.services.validation.base_validator import BaseValidator
from kin_txt_core.reports_building.domain.services.validation.factory_interface import BaseValidatorFactory
from kin_txt_core.reports_building.infrastructure.services import ModelTypesService

from kin_generic_builder.settings import Settings
from kin_generic_builder.validation.sklearn_validation import SkLearnModelValidator
from kin_generic_builder.validation.keras_validation import KerasModelValidator

__all__ = ["KinTxtDefaultValidationService", "get_validator_factory"]


class KinTxtDefaultValidationService(BaseValidatorFactory):
    _MODEL_TYPE_VALIDATOR_MAPPING: dict[ModelTypes, Type[SkLearnModelValidator | KerasModelValidator]] = {
        ModelTypes.SKLEARN: SkLearnModelValidator,
        ModelTypes.KERAS: KerasModelValidator,
    }

    def __init__(
        self,
        model_type_service: ModelTypesService,
        model_storage_path: str,
    ) -> None:
        self._model_type_service = model_type_service
        self._model_storage_path = model_storage_path

        self._logger = logging.getLogger(__name__)

    def create_validator(self, model: ModelEntity) -> BaseValidator:
        model_type_validator = self._MODEL_TYPE_VALIDATOR_MAPPING[model.model_type]

        return model_type_validator(self._model_storage_path)

    def is_handling_model_type(self, model_type: ModelTypes, model_code: str) -> bool:
        return model_type in self._MODEL_TYPE_VALIDATOR_MAPPING.keys()


def get_validator_factory() -> KinTxtDefaultValidationService:
    my_settings = Settings()
    default_settings = DefaultSettings()

    model_types_service = ModelTypesService(
        default_settings.model_types_service_url,
        kin_token=default_settings.kin_token,
    )

    return KinTxtDefaultValidationService(
        model_type_service=model_types_service,
        model_storage_path=my_settings.model_storage_path,
    )
