from numpy import ndarray
from keras.models import Sequential
from keras.utils import pad_sequences

from kin_news_core.reports_building.domain.entities import ModelEntity
from kin_news_core.reports_building.domain.services.predicting import IPredictor

from kin_generic_builder.predictor.preprocessing.service import TextPreprocessor


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

        padded_vectors = pad_sequences(vectors, maxlen=self._model.input_shape[1])
        prediction_result = self._model.predict(padded_vectors, verbose=False)[0]

        return self._get_predicted_news_type_label(prediction_result)

    def _get_predicted_news_type_label(self, prediction_result: ndarray) -> str:
        if self._model.layers[-1].units > 1:
            return self._metadata.category_mapping[str(prediction_result.argmax())]

        return self._metadata.category_mapping[str(round(prediction_result[0]))]
