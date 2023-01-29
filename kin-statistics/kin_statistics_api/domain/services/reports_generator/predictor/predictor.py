import pickle
from collections import Counter

import joblib

from kin_statistics_api.domain.services.reports_generator.predictor import (
    ISentimentAnalyzer,
    ITextPreprocessor,
    SentimentAnalyzer,
    IPredictor,
    TextPreprocessor,
)
from kin_statistics_api.constants import MessageCategories, SentimentTypes


class Predictor(IPredictor):
    def __init__(
        self,
        text_preprocessor: ITextPreprocessor,
        sentiment_analyzer: ISentimentAnalyzer,
        *,
        knn_model,
        svc_model,
        gaussian_model,
    ) -> None:
        self._text_preprocessor = text_preprocessor
        self._sentiment_analyzer = sentiment_analyzer

        self._knn_model = knn_model
        self._svc_model = svc_model
        self._gaussian_model = gaussian_model

        self._ml_models = [self._knn_model, self._svc_model, self._gaussian_model]

    def preprocess_text(self, text: str) -> str:
        return self._text_preprocessor.preprocess_text(text)

    def preprocess_and_lemmatize(self, text: str) -> str:
        return self._text_preprocessor.preprocess_and_lemmatize(text)

    def get_sentiment_type(self, text: str, news_type: MessageCategories, make_preprocessing: bool = False) -> SentimentTypes:
        if make_preprocessing:
            text = self._text_preprocessor.preprocess_and_lemmatize(text)

        return self._sentiment_analyzer.define_sentiment_type(text, news_type)

    def get_news_type(self, text: str) -> MessageCategories:
        ml_prediction_results = self._get_ml_models_predictions(text)

        counter = Counter([*ml_prediction_results])

        most_common_prediction = counter.most_common(1)[0][0]
        return most_common_prediction

    def _get_ml_models_predictions(self, text: str) -> tuple:
        test_vectors_for_ml_models = self._text_preprocessor.ml_vectorizing([text], make_preprocessing=True)

        # model.predict is going to return a list with a single value in it
        prediction_results = [model.predict(test_vectors_for_ml_models.toarray())[0] for model in self._ml_models]

        return tuple(map(self._get_predicted_news_type_label, prediction_results))

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
        sentiment_dictionary_path: str,
        stop_words_file_path: str,
        sklearn_vectorizer_path: str,
        knn_model_path: str,
        svc_model_path: str,
        gaussian_model_path: str,
    ) -> "Predictor":
        sklearn_vectorizer = pickle.load(open(sklearn_vectorizer_path, 'rb'))

        knn_model = joblib.load(open(knn_model_path, 'rb'))
        svc_model = joblib.load(open(svc_model_path, 'rb'))
        gaussian_model = joblib.load(open(gaussian_model_path, 'rb'))

        text_preprocessor = TextPreprocessor(sklearn_vectorizer=sklearn_vectorizer, stop_words_path=stop_words_file_path)
        sentiment_analyzer = SentimentAnalyzer(sentiment_dictionary_path)

        return cls(
            text_preprocessor=text_preprocessor,
            sentiment_analyzer=sentiment_analyzer,
            knn_model=knn_model,
            svc_model=svc_model,
            gaussian_model=gaussian_model
        )
