import logging
import random

import joblib
from sklearn import linear_model, ensemble, naive_bayes, neighbors, svm, tree, feature_extraction
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer

from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.exceptions import (
    UnableToLoadModelError,
    UnsupportedClassifierException,
    UnsupportedTokenizerException,
    UnableToLoadTokenizerError,
    ModelUnsupportedPredictionError,
    ModelPredictionError,
)
from kin_reports_generation.types import CategoryMapping

SK_SUPPORTED_MODELS_LIST = [
    *linear_model.__all__,
    *ensemble.__all__,
    *naive_bayes.__all__,
    *neighbors.__all__,
    *svm.__all__,
    *tree.__all__,
]

SK_SUPPORTED_TOKENIZERS_LIST = [
    feature_extraction.text.CountVectorizer.__class__.__name__,
    feature_extraction.text.TfidfVectorizer.__class__.__name__,
    feature_extraction.text.HashingVectorizer.__class__.__name__,
]


class SkLearnModelValidator:
    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def validate_model(self, model_entity: ModelEntity) -> None:
        try:
            model = joblib.load(model_entity.model_path)
        except Exception as error:
            self._logger.error(f"Unable to load model, with message: {error}")
            raise UnableToLoadModelError(
                f"Unable to load sklearn model from file. "
                f"Please make sure, that model file is valid joblib file."
            )

        model_name = model.__class__.__name__
        if model_name not in SK_SUPPORTED_MODELS_LIST:
            self._logger.error(f"Model of type {model_name} is not supported")
            raise UnsupportedClassifierException(
                f"Sklearn model was loaded, but it is not supported. "
                f"Kin-News currently is not able to use {model_name} model."
            )

        try:
            tokenizer = joblib.load(model_entity.tokenizer_path)
        except Exception as error:
            self._logger.error(f"Unable to load tokenizer, with message: {error}")
            raise UnableToLoadTokenizerError(
                f"Unable to load tokenizer model from file. "
                f"Please make sure, that tokenizer file is valid joblib file."
            )

        tokenizer_name = tokenizer.__class__.__name__
        if tokenizer_name not in SK_SUPPORTED_TOKENIZERS_LIST:
            raise UnsupportedTokenizerException(
                f"Tokenizer was loaded successfully, but it is not supported. "
                f"Kin-News currently is not able to use {tokenizer_name} tokenizer."
            )

        self._validate_predictions(model, tokenizer, model_entity.category_mapping)

    def _validate_predictions(
        self,
        model: svm.SVC,
        tokenizer: CountVectorizer | TfidfVectorizer | HashingVectorizer,
        category_mapping: CategoryMapping,
    ) -> None:
        vocab = tokenizer.get_feature_names_out()
        random_sentence = " ".join(random.choices(vocab, k=10))

        tokenized_sentence = tokenizer.transform([random_sentence])

        try:
            result = model.predict([tokenized_sentence])[0]
        except Exception as error:
            self._logger.error(f"Unable to predict with message: {error}")
            raise ModelPredictionError(
                f"Both model and tokenizer were loaded successfully, but exception occurred during test prediction. "
                f"Exception message: {error}."
            )

        if result not in category_mapping:
            self._logger.error(f"Model predicted category {result}, which is not in category mapping")
            raise ModelUnsupportedPredictionError(
                f"Both model and tokenizer were loaded successfully. "
                f"But model predicted category {result}, which is not in category mapping. "
                f"Please make sure, that model was trained with the same category mapping."
            )
