import logging
import random

import joblib
from scipy.sparse import csr_matrix

from kin_reports_generation.domain.entities import ModelEntity
from kin_reports_generation.domain.services.validation.interface import IModelValidation
from kin_reports_generation.domain.services.validation.sklearn_validation.supported_models import (
    SK_SUPPORTED_MODELS,
    SK_SUPPORTED_TOKENIZERS,
)
from kin_reports_generation.exceptions import (
    UnableToLoadModelError,
    UnsupportedClassifierException,
    UnsupportedTokenizerException,
    UnableToLoadTokenizerError,
    ModelUnsupportedPredictionError,
    ModelPredictionError,
)
from kin_reports_generation.types import CategoryMapping


class SkLearnModelValidator(IModelValidation):
    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def validate_model(self, model_entity: ModelEntity) -> None:
        try:
            model = joblib.load(model_entity.model_path)
            self._logger.info(f"[SkLearnModelValidator] {model_entity.owner_username} model was loaded successfully.")
        except Exception as error:
            self._logger.error(f"[SkLearnModelValidator] Unable to load model, with message: {str(error)}")
            raise UnableToLoadModelError(
                f"Unable to load sklearn model from file. "
                f"Please make sure, that model you've provided is a valid joblib file. "
            )

        model_name = model.__class__.__name__
        if model_name not in [_class.__name__ for _class in SK_SUPPORTED_MODELS]:
            self._logger.error(f"[SkLearnModelValidator] Model of type {model_name} is not supported")
            raise UnsupportedClassifierException(
                f"Sklearn model was loaded, but it is not supported. "
                f"Kin-News currently is not able to use {model_name} model. "
                f"The complete list of supported models can be found here: https://github.com/kinfi4/Kin-News"
            )

        self._logger.info(
            f"[SkLearnModelValidator] Model of {model_entity.owner_username} was checked to be supported ({model_name})."
        )

        try:
            tokenizer = joblib.load(model_entity.tokenizer_path)
            self._logger.info(f"[SkLearnModelValidator] {model_entity.owner_username} tokenizer was loaded successfully.")
        except Exception as error:
            self._logger.error(f"[SkLearnModelValidator] Unable to load tokenizer, with message: {str(error)}")
            raise UnableToLoadTokenizerError(
                f"Unable to load tokenizer model from file. "
                f"Please make sure, that tokenizer you've provided is a valid joblib file."
            )

        tokenizer_name = tokenizer.__class__.__name__
        if tokenizer_name not in [_class.__name__ for _class in SK_SUPPORTED_TOKENIZERS]:
            self._logger.error(f"[SkLearnModelValidator] Tokenizer of type {tokenizer_name} is not supported")
            raise UnsupportedTokenizerException(
                f"Tokenizer was loaded successfully, but it is not supported. "
                f"Kin-News currently is not able to use {tokenizer_name} tokenizer. "
                f"The complete list of supported tokenizers can be found here: https://github.com/kinfi4/Kin-News"
            )

        self._logger.info(
            f"[SkLearnModelValidator] {model_entity.owner_username} tokenizer was checked to be supported ({tokenizer_name})."
        )

        self._validate_predictions(model, tokenizer, model_entity.category_mapping)

    def _validate_predictions(
        self,
        model: SK_SUPPORTED_MODELS,
        tokenizer: SK_SUPPORTED_TOKENIZERS,
        category_mapping: CategoryMapping,
    ) -> None:
        vocab = tokenizer.get_feature_names_out()
        random_sentence = " ".join(random.choices(vocab, k=10))

        tokenized_sentence = tokenizer.transform([random_sentence])

        try:
            result = self._make_prediction(model, tokenized_sentence)
            self._logger.info(
                f"[SkLearnModelValidator] {model.__class__.__name__} model was checked to be working. "
                f"Prediction returned category {result}."
            )
        except Exception as error:
            self._logger.error(f"[SkLearnModelValidator] Unable to predict with message: {str(error)}")
            raise ModelPredictionError(
                f"Both model and tokenizer were loaded successfully, but exception occurred during test prediction. "
                f"Unexpected error is: {str(error)}. "
                f"Please make sure, that model was trained with the same tokenizer. Also make sure, that tokenizer is working as expected."
            )

        if result not in [int(category) for category in category_mapping.keys()]:
            self._logger.error(f"[SkLearnModelValidator] Model predicted category {result}, which is not in category mapping")
            raise ModelUnsupportedPredictionError(
                f"Both model and tokenizer were loaded successfully. "
                f"But model predicted category {result}, which is not in category mapping. "
                f"Please make sure, that model was trained with the same category mapping."
            )

        self._logger.info(f"[SkLearnModelValidator] {model.__class__.__name__} model was checked to be working with category mapping.")

    def _make_prediction(self, model: SK_SUPPORTED_MODELS, tokenized_message: csr_matrix) -> int:
        try:
            return model.predict(tokenized_message)[0]
        except Exception as error:
            if "dense data is required" in str(error):
                return model.predict(tokenized_message.toarray())[0]

            raise
