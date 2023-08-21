import joblib

from kin_reports_generation import Settings
from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.domain.services.predicting.preprocessing.preprocessor import TextPreprocessor
from kin_reports_generation.domain.services.predicting.predictor.interface import IPredictor
from kin_reports_generation.domain.services.predicting.vectorizer.vectorizer_factory import VectorizerFactory
from kin_reports_generation.exceptions import UnsupportedModelTypeError


class PredictorFactory:
    def __init__(
        self,
        model_entity: ModelEntity,
    ) -> None:
        self._model_entity = model_entity

    def create_predictor(self) -> IPredictor:
        text_preprocessor = self.create_text_preprocessor()

        if self._model_entity.model_type == ModelTypes.SKLEARN:
            return self._create_sk_learn_predictor(self._model_entity, text_preprocessor)
        if self._model_entity.model_type == ModelTypes.KERAS:
            return self._create_keras_predictor(self._model_entity, text_preprocessor)

        raise UnsupportedModelTypeError(f"Model type {self._model_entity.model_type} is not supported")

    def create_text_preprocessor(self) -> TextPreprocessor:
        vectorizer_factory = VectorizerFactory()
        vectorizer = vectorizer_factory.create_vectorizer(self._model_entity)

        return TextPreprocessor(
            stop_words_path=Settings().default_stop_words_path,
            vectorizer=vectorizer,
        )

    def _create_sk_learn_predictor(self, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> IPredictor:
        from kin_reports_generation.domain.services.predicting.predictor.types import SkLearnPredictor

        model = joblib.load(model_metadata.model_path)

        return SkLearnPredictor(
            model=model,
            model_metadata=model_metadata,
            text_preprocessor=text_preprocessor,
        )

    def _create_keras_predictor(self, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> IPredictor:
        pass
