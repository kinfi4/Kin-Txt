import pickle
import logging
import random

from keras import models
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

from kin_news_core.reports_building.domain.entities import ModelEntity
from kin_news_core.reports_building.domain.services.validation.base_validator import BaseValidator
from kin_news_core.reports_building.exceptions import (
    UnableToLoadModelError,
    UnsupportedClassifierException,
    UnsupportedTokenizerException,
    UnableToLoadTokenizerError,
    ModelUnsupportedPredictionError,
    ModelPredictionError, BaseValidationError,
)
from kin_news_core.reports_building.types import CategoryMapping, ValidationResult
from kin_reports_generation.mixins import UnpackKerasArchiveMixin

from kin_reports_generation.validation.keras_validation.supported_models import (
    KERAS_SUPPORTED_TOKENIZERS,
    KERAS_SUPPORTED_MODELS,
)


class KerasModelValidator(BaseValidator, UnpackKerasArchiveMixin):
    def __init__(self, model_storage_path: str) -> None:
        self._model_storage_path = model_storage_path

        self._logger = logging.getLogger(self.__class__.__name__)

    def validate_model(self, model: ModelEntity) -> ValidationResult:
        try:
            self._validate_model(model)
        except BaseValidationError as error:
            return False, str(error)

        return True, None

    def _validate_model(self, model_entity: ModelEntity) -> None:
        self._unpack_archive_if_needed(model_entity.get_model_binaries_path(self._model_storage_path))

        try:
            model = load_model(model_entity.get_model_binaries_path(self._model_storage_path))
            self._logger.info(f"[KerasModelValidator] {model_entity.owner_username} model was loaded successfully.")
        except Exception as error:
            self._logger.error(f"[KerasModelValidator] Unable to load model, with message: {str(error)}")
            raise UnableToLoadModelError(
                f"Unable to load keras model from file. "
                f"Please make sure, that model you've provided is a valid keras file or an archive of keras model. "
            )

        model_name = model.__class__.__name__
        if model_name not in [_class.__name__ for _class in KERAS_SUPPORTED_MODELS]:
            self._logger.error(f"[KerasModelValidator] Model of type {model_name} is not supported")
            raise UnsupportedClassifierException(
                f"Keras model was loaded, but it is not supported. "
                f"Kin-News currently is not able to use {model_name} model. "
                f"The complete list of supported models can be found here: https://github.com/kinfi4/Kin-News"
            )

        self._logger.info(
            f"[KerasModelValidator] Model of {model_entity.owner_username} was checked to be supported ({model_name})."
        )

        try:
            with open(model_entity.get_tokenizer_binaries_path(self._model_storage_path), "rb") as tokenizer_file:
                tokenizer = pickle.load(tokenizer_file)

            self._logger.info(f"[KerasModelValidator] {model_entity.owner_username} tokenizer was loaded successfully.")
        except Exception as error:
            self._logger.error(f"[KerasModelValidator] Unable to load tokenizer, with message: {str(error)}")
            raise UnableToLoadTokenizerError(
                f"Unable to load tokenizer model from file. "
                f"Please make sure, that tokenizer you've provided is a valid pickle file."
            )

        tokenizer_name = tokenizer.__class__.__name__
        if tokenizer_name not in [_class.__name__ for _class in KERAS_SUPPORTED_TOKENIZERS]:
            self._logger.error(f"[KerasModelValidator] Tokenizer of type {tokenizer_name} is not supported")
            raise UnsupportedTokenizerException(
                f"Tokenizer was loaded successfully, but it is not supported. "
                f"Kin-News currently is not able to use {tokenizer_name} tokenizer. "
                f"The complete list of supported tokenizers can be found here: https://github.com/kinfi4/Kin-News"
            )

        self._logger.info(
            f"[KerasModelValidator] {model_entity.owner_username} tokenizer was checked to be supported ({tokenizer_name})."
        )

        self._validate_predictions(model, tokenizer, model_entity.category_mapping)

    def _validate_predictions(
        self,
        model: models.Sequential,
        tokenizer: Tokenizer,
        category_mapping: CategoryMapping,
    ) -> None:
        vocab = list(tokenizer.word_index.keys())
        random_sentence = " ".join(random.choices(vocab, k=10))

        tokenized_sentence = tokenizer.texts_to_sequences([random_sentence])
        tokenized_sentence = pad_sequences(tokenized_sentence, maxlen=model.input_shape[1])

        try:
            result = model.predict(tokenized_sentence)[0].argmax()
            self._logger.info(
                f"[KerasModelValidator] {model.__class__.__name__} model was checked to be working. "
                f"Prediction returned category {result}."
            )
        except Exception as error:
            self._logger.error(f"[KerasModelValidator] Unable to predict with message: {str(error)}")
            raise ModelPredictionError(
                f"Both model and tokenizer were loaded successfully, but exception occurred during test prediction. "
                f"Unexpected error is: {str(error)}. "
                f"Please make sure, that model was trained with the same tokenizer. Also make sure, that tokenizer is working as expected."
            )

        if result not in [int(category) for category in category_mapping.keys()]:
            self._logger.error(f"[KerasModelValidator] Model predicted category {result}, which is not in category mapping")
            raise ModelUnsupportedPredictionError(
                f"Both model and tokenizer were loaded successfully. "
                f"But model predicted category {result}, which is not in category mapping. "
                f"Please make sure, that model was trained with the same category mapping."
            )

        self._logger.info(f"[KerasModelValidator] {model.__class__.__name__} model was checked to be working with category mapping.")
