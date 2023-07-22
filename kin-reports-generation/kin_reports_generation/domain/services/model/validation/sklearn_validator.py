import random

import joblib
import sklearn as sk
from sklearn import linear_model, ensemble, naive_bayes, neighbors, svm, tree, feature_extraction
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer

from kin_reports_generation.domain.entities import CreateModelEntity
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
    def validate_model(self, create_model_entity: CreateModelEntity) -> None:
        try:
            model = joblib.load(create_model_entity.model_path)
        except Exception as error:
            raise UnableToLoadModelError(f"Unable to load model, with message: {error}")

        model_name = model.__class__.__name__
        if model_name not in SK_SUPPORTED_MODELS_LIST:
            raise UnsupportedClassifierException(f"Model of type {model_name} is not supported", model_type=model_name)

        try:
            tokenizer = joblib.load(create_model_entity.tokenizer_path)
        except Exception as error:
            raise UnableToLoadTokenizerError(f"Unable to load tokenizer with message: {error}")

        tokenizer_name = tokenizer.__class__.__name__
        if tokenizer_name not in SK_SUPPORTED_TOKENIZERS_LIST:
            raise UnsupportedTokenizerException(f"Tokenizer of type {tokenizer_name} is not supported", tokenizer_type=tokenizer_name)

        self._validate_predictions(model, tokenizer, create_model_entity.category_list)

    def _validate_predictions(
        self,
        model: svm.SVC,
        tokenizer: CountVectorizer | TfidfVectorizer | HashingVectorizer,
        category_list: list[CategoryMapping],
    ) -> None:
        vocab = tokenizer.get_feature_names_out()
        random_sentence = " ".join(random.choices(vocab, k=10))

        tokenized_sentence = tokenizer.transform([random_sentence])

        try:
            result = model.predict([tokenized_sentence])[0]
        except Exception as error:
            raise ModelPredictionError(f"Unable to predict with message: {error}")

        if result not in category_list:
            raise ModelUnsupportedPredictionError(prediction_type=result)
