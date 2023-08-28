from keras.models import Sequential

from kin_news_core.reports_building.domain.entities import ModelEntity
from kin_news_core.reports_building.domain.services.predicting import IPredictor

from kin_reports_generation.predictor.preprocessing.service import TextPreprocessor


class KerasPredictor(IPredictor):
    def __init__(self, model: Sequential, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> None:
        self._text_preprocessor = text_preprocessor
        self._model = model
        self._metadata = model_metadata

    def preprocess_text(self, text: str) -> str:
        return self._text_preprocessor.preprocess_text(text)

    def preprocess_and_lemmatize(self, text: str) -> str:
        return self._text_preprocessor.preprocess_and_lemmatize(text)

    def predict(self, text: str) -> str:
        vectors = self._text_preprocessor.vectorize([text])

        prediction_result = self._model.predict(vectors.toarray())[0]
        return self._get_predicted_news_type_label(prediction_result)

    def _get_predicted_news_type_label(self, prediction_result: int) -> str:
        return self._metadata.category_mapping[str(prediction_result)]
