from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor

from kin_builtin_models.predictor.predictors.news_classification.preprocessor import NewsClassificationPreprocessor


class NewsClassificationBertPredictor(IPredictor):
    model_code: str = "ua-ner"
    mapping: dict[str, str] = {
        "LOC": "Location",
        "ORG": "Organization",
        "PER": "Person",
    }

    def __init__(self, preprocessor: NewsClassificationPreprocessor):
        super().__init__()
        self.preprocessor = preprocessor

    def predict_post(self, entity: ClassificationEntity) -> str:
        pass

    def predict_post_tokens(self, entity: ClassificationEntity) -> dict[str, list[str]]:
        raise NotImplementedError("News classification model doesn't support token prediction")

    def preprocess_text(self, text: str) -> str:
        return self.preprocessor.preprocess_text(text)
