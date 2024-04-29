import os
import re

import tensorflow as tf
from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertModel

preprocessing_sub_regexes: list[re.Pattern] = [
    re.compile(r"\*\*|__|~~"),
    re.compile(r'""'),
    re.compile(r'["“”«»„"]\s*["“”«»„"]'),
    re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"),
    re.compile(r"\n|\r|\t"),
    re.compile(r"\[|\]"),
    re.compile(r"\(\s*\)"),
    # re.compile(r"\s+"),
    re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        re.UNICODE,
    ),
]


class NewsClassificationBertPredictor:
    MAX_LENGTH = 360

    model_code: str = "bert_news_classification"
    mapping: dict[str, str] = {
        "0": "Corruption",
        "1": "Crisis",
        "2": "Economical",
        "3": "Other",
        "4": "Political",
    }

    def __init__(self, models_storage_path: str) -> None:
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-uncased")

        news_classification_model_path = os.path.join(models_storage_path, "news-classification-model")
        self.model = load_model(news_classification_model_path, custom_objects={"TFBertModel": TFBertModel})

    def predict_post(self, txt: str) -> str:
        preprocessed_text = self.preprocess_text(txt)

        input_ids, attention_mask = self._text_to_tokens(preprocessed_text)

        prediction_index = self.model.predict(
            {
                "input_ids": tf.expand_dims(input_ids, 0),
                "attention_mask": tf.expand_dims(attention_mask, 0),
            },
            verbose=False,
        ).argmax()

        return self.mapping[str(prediction_index)]

    def preprocess_text(self, text: str) -> str:
        for regex in preprocessing_sub_regexes:
            text = regex.sub("", text)

        return text.lower().strip()

    def _text_to_tokens(self, text: str) -> tuple[tf.Tensor, tf.Tensor]:
        inputs = self.tokenizer.encode_plus(
            text,
            return_tensors="tf",
            max_length=360,
            padding='max_length',
            truncation=True,
        )

        return inputs["input_ids"][0], inputs["attention_mask"][0]
