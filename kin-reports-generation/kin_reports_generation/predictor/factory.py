import joblib
from keras.models import load_model

from kin_news_core.reports_building.constants import ModelTypes
from kin_news_core.reports_building.domain.entities import ModelEntity
from kin_news_core.reports_building.domain.services.predicting import IPredictorFactory, IPredictor
from kin_news_core.reports_building.exceptions import UnsupportedModelTypeError

from kin_reports_generation.predictor.preprocessing.service import TextPreprocessor
from kin_reports_generation.predictor.vectorizer.vectorizer_factory import VectorizerFactory
from kin_reports_generation.settings import Settings
from kin_reports_generation.mixins import UnpackArchiveMixin

__all__ = ["KinTxtDefaultPredictorFactory"]


class KinTxtDefaultPredictorFactory(UnpackArchiveMixin, IPredictorFactory):
    def create_predictor(self, model_entity: ModelEntity) -> IPredictor:
        text_preprocessor = self.create_text_preprocessor(model_entity)

        if model_entity.model_type == ModelTypes.SKLEARN:
            return self._create_sk_learn_predictor(model_entity, text_preprocessor)
        if model_entity.model_type == ModelTypes.KERAS:
            return self._create_keras_predictor(model_entity, text_preprocessor)

        raise UnsupportedModelTypeError(f"Model type {model_entity.model_type} is not supported")

    def create_text_preprocessor(self, model_entity: ModelEntity) -> TextPreprocessor:
        vectorizer_factory = VectorizerFactory(Settings().model_storage_path)
        vectorizer = vectorizer_factory.create_vectorizer(model_entity)

        return TextPreprocessor(
            stop_words_path=Settings().default_stop_words_path,
            vectorizer=vectorizer,
        )

    def is_handling(self, model_type: ModelTypes, model_code: str) -> bool:
        return model_type in (ModelTypes.SKLEARN, ModelTypes.KERAS)

    def _create_sk_learn_predictor(self, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> IPredictor:
        from kin_reports_generation.predictor.predictor_types.sklearn_predictor import SkLearnPredictor

        model = joblib.load(model_metadata.get_model_binaries_path(Settings().model_storage_path))

        return SkLearnPredictor(
            model=model,
            model_metadata=model_metadata,
            text_preprocessor=text_preprocessor,
        )

    def _create_keras_predictor(self, model_metadata: ModelEntity, text_preprocessor: TextPreprocessor) -> IPredictor:
        from kin_reports_generation.predictor.predictor_types.keras_predictor import KerasPredictor

        self._unpack_archive_if_needed(model_metadata.get_model_binaries_path(Settings().model_storage_path))

        model = load_model(model_metadata.get_model_binaries_path(Settings().model_storage_path))

        return KerasPredictor(
            model=model,
            model_metadata=model_metadata,
            text_preprocessor=text_preprocessor,
        )
