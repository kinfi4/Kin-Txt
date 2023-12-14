from kin_txt_core.datasources.common import ClassificationEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor


class NewsTypePredictor(IPredictor):
    def predict(self, entity: ClassificationEntity) -> str:
        return "Political"

    def preprocess_text(self, text: str) -> str:
        return text

    def preprocess_and_lemmatize(self, text: str) -> str:
        return text
