from kin_txt_core.datasources.common import ClassificationEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor


class EnglishSentimentPredictor(IPredictor):
    def predict(self, entity: ClassificationEntity) -> str:
        return "Negative"

    def preprocess_text(self, text: str) -> str:
        return text
