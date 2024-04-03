from kin_builtin_models.predictor.predictors.news_classification import (
    NewsClassificationBertPredictor,
    NewsClassificationPreprocessor,
)
from kin_builtin_models.predictor.predictors.ukranian_ner import UaNerPredictor
from kin_builtin_models.settings import Settings

from kin_txt_core.reports_building.constants import ModelTypes
from kin_txt_core.reports_building.domain.entities import (
    ModelEntity,
    CustomModelRegistrationEntity,
    PreprocessingConfig,
    GenerateReportEntity,
)
from kin_txt_core.reports_building.domain.services.predicting import IPredictorFactory, IPredictor

__all__ = ["BuiltInModelsPredictorFactory"]


class BuiltInModelsPredictorFactory(IPredictorFactory):
    model_types: list[CustomModelRegistrationEntity] = [
        CustomModelRegistrationEntity(
            code=NewsClassificationBertPredictor.model_code,
            name="News Classification Model",
            owner_username="kinfi4",
            category_mapping=NewsClassificationBertPredictor.mapping,
            preprocessing_config=PreprocessingConfig(),
        ),
        CustomModelRegistrationEntity(
            code=UaNerPredictor.model_code,
            name="NER Model for Ukrainian language",
            owner_username="kinfi4",
            category_mapping=UaNerPredictor.mapping,
            preprocessing_config=PreprocessingConfig(),
        ),
    ]

    def create_predictor(self, model_entity: ModelEntity, generation_request: GenerateReportEntity) -> IPredictor:
        if model_entity.code == NewsClassificationBertPredictor.model_code:
            return NewsClassificationBertPredictor(
                models_storage_path=Settings().model_storage_path,
                report_type=generation_request.report_type,
                preprocessor=NewsClassificationPreprocessor(),
            )

        if model_entity.code == UaNerPredictor.model_code:
            return UaNerPredictor(generation_request.report_type)

        raise ValueError(f"Model with code {model_entity.code} is not supported")

    def is_handling(self, model_type: ModelTypes, model_code: str) -> bool:
        return model_type == ModelTypes.BUILTIN and model_code in self.supported_model_type_codes

    @property
    def supported_model_type_codes(self) -> list[str]:
        return [model_type.code for model_type in self.model_types]
