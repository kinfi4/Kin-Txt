import pickle

from sklearn.preprocessing import LabelEncoder
from transformers import TFBertForSequenceClassification, BertTokenizer


class ModelLoader:
    def __init__(self, model_path: str, tokenizer_path: str, label_encoder_path: str) -> None:
        self._model_path = model_path
        self._tokenizer_path = tokenizer_path
        self._label_encoder_path = label_encoder_path

    def load_model(self) -> TFBertForSequenceClassification:
        return TFBertForSequenceClassification.from_pretrained(self._model_path)

    def load_tokenizer(self) -> BertTokenizer:
        return BertTokenizer.from_pretrained(self._tokenizer_path)

    def load_label_encoder(self) -> LabelEncoder:
        with open(self._label_encoder_path, "rb") as label_encoder_file:
            loaded_label_encoder = pickle.load(label_encoder_file)

        return loaded_label_encoder
