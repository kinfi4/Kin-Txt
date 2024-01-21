from sklearn.svm import SVC

from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.domain.entities import ModelEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor
from kin_generic_builder.predictor.preprocessing.service import TextPreprocessor


class SkLearnPredictor(IPredictor):
    def __init__(self, model: SVC, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> None:
        self._text_preprocessor = text_preprocessor
        self._model = model
        self._metadata = model_metadata

    def preprocess_text(self, text: str) -> str:
        return self._text_preprocessor.preprocess_text(text)

    def predict(self, entity: ClassificationEntity) -> str:
        vectors = self._text_preprocessor.vectorize([entity.text], preprocess=True)

        prediction_result = self._model.predict(vectors.toarray())[0]
        return self._get_predicted_news_type_label(prediction_result)

    def _get_predicted_news_type_label(self, prediction_result: int) -> str:
        return self._metadata.category_mapping[str(prediction_result)]
