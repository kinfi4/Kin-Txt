from numpy import ndarray
from keras.models import Sequential
from keras.utils import pad_sequences

from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.domain.entities import ModelEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor

from kin_generic_builder.predictor.preprocessing.service import TextPreprocessor


class KerasPredictor(IPredictor):
    def predict_post(self, entity: ClassificationEntity) -> str:
        vectors = self._text_preprocessor.vectorize([entity.text], preprocess=True)

        maxlen = self._model.input_shape[1]
        if self._metadata.preprocessing_config.max_tokens is not None:
            maxlen = self._metadata.preprocessing_config.max_tokens

        padded_vectors = pad_sequences(
            vectors,
            maxlen=maxlen,
            padding=self._metadata.preprocessing_config.padding,
            truncating=self._metadata.preprocessing_config.truncating,
        )

        prediction_result = self._model.predict(padded_vectors, verbose=False)[0]

        return self._predict(prediction_result)

    def predict_post_tokens(self, entity: ClassificationEntity) -> dict[str, list[str]]:
        raise NotImplementedError("This method is not implemented for KerasPredictor")

    def __init__(self, model: Sequential, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> None:
        self._text_preprocessor = text_preprocessor
        self._model = model
        self._metadata = model_metadata

    def preprocess_text(self, text: str) -> str:
        return self._text_preprocessor.preprocess_text(text)

    def _predict(self, prediction_result: ndarray) -> str:
        if self._model.layers[-1].units > 1:
            return self._metadata.category_mapping[str(prediction_result.argmax())]

        return self._metadata.category_mapping[str(round(prediction_result[0]))]
