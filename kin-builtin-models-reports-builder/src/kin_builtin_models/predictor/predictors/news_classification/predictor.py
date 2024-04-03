import os
import logging

import tensorflow as tf
from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertModel

from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.constants import ReportTypes
from kin_txt_core.reports_building.domain.services.predicting import IPredictor

from kin_builtin_models.predictor.predictors.news_classification.preprocessor import NewsClassificationPreprocessor


class NewsClassificationBertPredictor(IPredictor):
    MAX_LENGTH = 360

    model_code: str = "bert_news_classification"
    mapping: dict[str, str] = {
        "0": "Corruption",
        "1": "Crisis",
        "2": "Economical",
        "3": "Other",
        "4": "Political",
    }

    def __init__(
        self,
        models_storage_path: str,
        report_type: ReportTypes,
        preprocessor: NewsClassificationPreprocessor,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._predicted_items_counter = 0

        self._report_type = report_type
        self.preprocessor = preprocessor

        self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-uncased")

        news_classification_model_path = os.path.join(models_storage_path, "news-classification-model")
        self.model = load_model(news_classification_model_path, custom_objects={"TFBertModel": TFBertModel})

    def predict_post(self, entity: ClassificationEntity) -> str:
        if self._predicted_items_counter % 250 == 0:
            self._logger.info(
                f"[NewsClassificationBertPredictor] Predicted {self._predicted_items_counter} items so far..."
            )

        preprocessed_text = self.preprocessor.preprocess_text(
            entity.text,
            lemmatize=False,
        )

        input_ids, attention_mask = self._text_to_tokens(preprocessed_text)

        prediction_index = self.model.predict(
            {
                "input_ids": tf.expand_dims(input_ids, 0),
                "attention_mask": tf.expand_dims(attention_mask, 0),
            },
            verbose=False,
        ).argmax()

        self._predicted_items_counter += 1

        return self.mapping[str(prediction_index)]

    def predict_post_tokens(self, entity: ClassificationEntity) -> dict[str, list[str]]:
        raise NotImplementedError("News classification model doesn't support token prediction")

    def preprocess_text(self, text: str) -> str:
        return self.preprocessor.preprocess_text(
            text,
            lemmatize=self._report_type == ReportTypes.WORD_CLOUD,
        )

    def _text_to_tokens(self, text: str) -> tuple[tf.Tensor, tf.Tensor]:
        inputs = self.tokenizer.encode_plus(
            text,
            return_tensors="tf",
            max_length=360,
            padding='max_length',
            truncation=True,
        )

        return inputs["input_ids"][0], inputs["attention_mask"][0]
