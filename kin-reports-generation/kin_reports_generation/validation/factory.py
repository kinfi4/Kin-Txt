import os
import logging
from typing import Type

from kin_news_core.reports_building.constants import ModelTypes
from kin_news_core.reports_building.settings import Settings as DefaultSettings
from kin_news_core.reports_building.domain.entities import ModelEntity
from kin_news_core.reports_building.domain.services.validation.base_validator import BaseValidator
from kin_news_core.reports_building.domain.services.validation.factory_interface import BaseValidatorFactory
from kin_news_core.reports_building.infrastructure.services import ModelTypesService

from kin_reports_generation import Settings
from kin_reports_generation.validation.sklearn_validation import SkLearnModelValidator
from kin_reports_generation.validation.keras_validation import KerasModelValidator

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
        self.__preload_model_binaries(model)
        model_type_validator = self._MODEL_TYPE_VALIDATOR_MAPPING[model.model_type]

        return model_type_validator(self._model_storage_path)

    def __preload_model_binaries(self, model: ModelEntity) -> None:
        self._logger.info(f"[ModelService] Preloading model binaries for {model.code}")

        model_data = self._model_type_service.get_model_binaries(model.owner_username, model.code)
        tokenizer_data = self._model_type_service.get_tokenizer_binaries(model.owner_username, model.code)

        user_model_storage_path = model.get_model_directory_path(self._model_storage_path)
        if not os.path.exists(user_model_storage_path):
            os.makedirs(user_model_storage_path)

        model_path = model.get_model_binaries_path(self._model_storage_path)
        with open(model_path, "wb") as model_file:
            model_file.write(model_data.read())

        tokenizer_path = model.get_tokenizer_binaries_path(self._model_storage_path)
        with open(tokenizer_path, "wb") as tokenizer_file:
            tokenizer_file.write(tokenizer_data.read())


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
