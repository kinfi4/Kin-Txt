import re

import emoji
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from transformers import TFBertForSequenceClassification, PreTrainedTokenizerBase

from .model_loader import ModelLoader


def _remove_emojis(text: str) -> str:
    text_no_emoji = emoji.demojize(text)
    emoji_pattern = re.compile(":[A-Za-z_]+?:")
    return emoji_pattern.sub(r'', text_no_emoji)


def _preprocess_texts(texts: pd.Series) -> pd.Series:
    texts = texts.str.lower()
    texts = texts.str.replace(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "")
    texts = texts.str.replace(r"@\S+", "")
    texts = texts.apply(_remove_emojis)

    return texts


def _predict_texts(
    texts: pd.Series,
    model: TFBertForSequenceClassification,
    tokenizer: PreTrainedTokenizerBase,
    label_encoder: LabelEncoder,
) -> tuple[list[str], pd.Series]:
    texts = _preprocess_texts(texts)
    encodings = tokenizer(texts.tolist(), truncation=True, padding="max_length", max_length=512)

    input_dict = {
        "input_ids": tf.constant(encodings["input_ids"]),
        "attention_mask": tf.constant(encodings["attention_mask"])
    }

    logits = model.predict(input_dict).logits

    probabilities = tf.nn.softmax(logits).numpy()
    class_idx = np.argmax(probabilities, axis=1)

    predicted_class = label_encoder.inverse_transform(class_idx)

    return predicted_class, texts


def make_predictions(
    file_path: str,
    model_path: str,
    tokenizer_path: str,
    label_encoder_path: str,
) -> None:
    print("Loading model, tokenizer and label encoder...")

    model_loader = ModelLoader(model_path, tokenizer_path, label_encoder_path)

    model = model_loader.load_model()
    tokenizer = model_loader.load_tokenizer()
    label_encoder = model_loader.load_label_encoder()

    df = pd.read_csv(file_path)

    print("Predicting labels...")

    df["label"], df["text"] = _predict_texts(df["text"], model, tokenizer, label_encoder)
    df.to_csv(file_path.replace(".csv", "__predicted.csv"), index=False)

    print("Predictions saved to file.")
