import pickle

import joblib

from kin_reports_generation.domain.services.predictor import (
    IPredictor,
    TextPreprocessor,
    ITextPreprocessor,
)
from kin_reports_generation.constants import MessageCategories


class NewsCategoryPredictor(IPredictor, ITextPreprocessor):
    def __init__(
        self,
        text_preprocessor: TextPreprocessor,
        *,
        svc_model,
    ) -> None:
        self._text_preprocessor = text_preprocessor

        self._svc_model = svc_model

    def preprocess_text(self, text: str) -> str:
        return self._text_preprocessor.preprocess_text(text)

    def preprocess_and_lemmatize(self, text: str) -> str:
        return self._text_preprocessor.preprocess_and_lemmatize(text)

    def get_category(self, text: str) -> MessageCategories:
        test_vectors_for_ml_models = self._text_preprocessor.ml_vectorizing([text], make_preprocessing=True)

        prediction_result = self._svc_model.predict(test_vectors_for_ml_models.toarray())[0]
        return self._get_predicted_news_type_label(prediction_result)

    @staticmethod
    def _get_predicted_news_type_label(label_idx: int) -> MessageCategories:
        labels_indexes = {
            0: MessageCategories.ECONOMICAL,
            1: MessageCategories.POLITICAL,
            2: MessageCategories.SHELLING,
            3: MessageCategories.HUMANITARIAN,
        }

        if label_idx not in labels_indexes:
            raise AttributeError(f'The value of label_idx must be between 0 and 3, got label_idx = {label_idx}')

        return labels_indexes[label_idx]

    @classmethod
    def create_from_files(
        cls,
        stop_words_file_path: str,
        sklearn_vectorizer_path: str,
        svc_model_path: str,
    ) -> "NewsCategoryPredictor":
        sklearn_vectorizer = pickle.load(open(sklearn_vectorizer_path, 'rb'))

        svc_model = joblib.load(open(svc_model_path, 'rb'))

        text_preprocessor = TextPreprocessor(sklearn_vectorizer=sklearn_vectorizer, stop_words_path=stop_words_file_path)

        return cls(
            text_preprocessor=text_preprocessor,
            svc_model=svc_model,
        )
