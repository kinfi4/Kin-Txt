import joblib

from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.domain.services.predicting.vectorizer.types import SklearnVectorizer
from kin_reports_generation.domain.services.predicting.vectorizer.interface import ITextVectorizer
from kin_reports_generation.constants import ModelTypes


class VectorizerFactory:
    def create_vectorizer(self, model: ModelEntity) -> ITextVectorizer:
        if model.model_type == ModelTypes.SKLEARN:
            return self._build_sklearn_vectorizer(model)

    def _build_sklearn_vectorizer(self, model: ModelEntity) -> SklearnVectorizer:
        loaded_vectorizer_model = joblib.load(model.tokenizer_path)

        return SklearnVectorizer(loaded_vectorizer_model)
