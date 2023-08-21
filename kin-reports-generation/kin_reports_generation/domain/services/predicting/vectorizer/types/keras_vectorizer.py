from typing import Iterable

from keras.preprocessing.text import Tokenizer

from kin_reports_generation.domain.services.predicting.vectorizer.interface import ITextVectorizer


class KerasVectorizer(ITextVectorizer):
    def __init__(self, vectorizer: Tokenizer) -> None:
        self._vectorizer = vectorizer

    def vectorize(self, texts: Iterable[str]) -> list:
        return self._vectorizer.texts_to_sequences(texts)
