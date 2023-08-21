import joblib
import pickle

from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.domain.services.predicting.vectorizer.types import SklearnVectorizer, KerasVectorizer
from kin_reports_generation.domain.services.predicting.vectorizer.interface import ITextVectorizer
from kin_reports_generation.constants import ModelTypes


class VectorizerFactory:
    def create_vectorizer(self, model: ModelEntity) -> ITextVectorizer:
        if model.model_type == ModelTypes.SKLEARN:
            return self._build_sklearn_vectorizer(model)
        if model.model_type == ModelTypes.KERAS:
            return self._build_keras_vectorizer(model)

        raise NotImplemented("Model type is not supported")

    def _build_sklearn_vectorizer(self, model: ModelEntity) -> SklearnVectorizer:
        loaded_vectorizer_model = joblib.load(model.tokenizer_path)

        return SklearnVectorizer(loaded_vectorizer_model)

    def _build_keras_vectorizer(self, model: ModelEntity) -> KerasVectorizer:
        with open(model.tokenizer_path, "rb") as tokenizer_file:
            loaded_vectorizer_model = pickle.load(tokenizer_file)

        return KerasVectorizer(loaded_vectorizer_model)
