from kin_builtin_models.predictor.english_sentiment_predictor import EnglishSentimentPredictor

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
            code="english-sentiment-classification-bert-sst-2",
            name="English Sentiment classification BERT SST-2",
            owner_username="kinfi4",
            category_mapping={
                "0": "Negative",
                "1": "Positive",
            },
            preprocessing_config=PreprocessingConfig(),
        ),
    ]

    def create_predictor(self, model_entity: ModelEntity, generation_request: GenerateReportEntity) -> IPredictor:
        return EnglishSentimentPredictor(report_type=generation_request.report_type)

    def is_handling(self, model_type: ModelTypes, model_code: str) -> bool:
        return model_type == ModelTypes.BUILTIN and model_code in self.supported_model_type_codes

    @property
    def supported_model_type_codes(self) -> list[str]:
        return [model_type.code for model_type in self.model_types]
