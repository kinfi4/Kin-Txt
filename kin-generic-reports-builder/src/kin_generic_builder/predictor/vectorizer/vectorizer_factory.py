import joblib
import pickle

from kin_txt_core.reports_building.constants import ModelTypes
from kin_txt_core.reports_building.domain.entities import ModelEntity

from kin_generic_builder.predictor.vectorizer.types import SklearnVectorizer, KerasVectorizer
from kin_generic_builder.predictor.vectorizer.interface import ITextVectorizer


class VectorizerFactory:
    def __init__(self, model_storage_path: str) -> None:
        self._model_storage_path = model_storage_path

    def create_vectorizer(self, model: ModelEntity) -> ITextVectorizer:
        if model.model_type == ModelTypes.SKLEARN:
            return self._build_sklearn_vectorizer(model)
        if model.model_type == ModelTypes.KERAS:
            return self._build_keras_vectorizer(model)

        raise NotImplementedError("Model type is not supported")

    def _build_sklearn_vectorizer(self, model: ModelEntity) -> SklearnVectorizer:
        loaded_vectorizer_model = joblib.load(model.get_tokenizer_binaries_path(self._model_storage_path))

        return SklearnVectorizer(loaded_vectorizer_model)

    def _build_keras_vectorizer(self, model: ModelEntity) -> KerasVectorizer:
        with open(model.get_tokenizer_binaries_path(self._model_storage_path), "rb") as tokenizer_file:
            loaded_vectorizer_model = pickle.load(tokenizer_file)

        return KerasVectorizer(loaded_vectorizer_model)
