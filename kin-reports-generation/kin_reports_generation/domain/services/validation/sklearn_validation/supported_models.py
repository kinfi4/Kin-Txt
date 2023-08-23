from keras import models
from keras.preprocessing.text import Tokenizer


KERAS_SUPPORTED_MODELS = (
    models.Sequential,
)

KERAS_SUPPORTED_TOKENIZERS = (
    Tokenizer,
)
