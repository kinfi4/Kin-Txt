import json
import re
from string import punctuation
from typing import Iterable, Any

import pandas as pd
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from scipy.sparse.csr import csr_matrix

from kin_reports_generation.domain.services.predicting import ITextPreprocessor
from kin_reports_generation.constants import MAX_POST_LEN_IN_WORDS, emoji_regex_compiled
from kin_reports_generation.domain.services.predicting.vectorizer.interface import ITextVectorizer


class TextPreprocessor(ITextPreprocessor, ITextVectorizer):
    def __init__(
        self,
        stop_words_path: str,
        vectorizer: ITextVectorizer,
        morph: MorphAnalyzer | None = None,
    ) -> None:
        self._morph = morph if morph else MorphAnalyzer()
        self._vectorizer = vectorizer

        self._russian_stop_words = self._init_stop_words(stop_words_path)

    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = self.remove_html_tags(text)
        text = self.remove_links(text)
        text = self.remove_emoji(text)
        text = self.remove_punctuation(text)
        text = self.remove_stop_words(text, self._russian_stop_words)
        text = self.remove_extra_spaces(text)

        return text

    def preprocess_and_lemmatize(self, text: str) -> str:
        text = self.preprocess_text(text)
        tokens = word_tokenize(text, language='russian')

        return ' '.join((self._morph.parse(word)[0].normal_form for word in tokens))

    def vectorize(self, texts: Iterable[str]) -> csr_matrix:
        texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
        texts = texts.apply(self.preprocess_and_lemmatize)

        return self._vectorizer.vectorize(texts)

    @staticmethod
    def remove_html_tags(text: str) -> str:
        return re.sub(r'<[^>]+>', ' ', text)

    @staticmethod
    def remove_links(text: str) -> str:
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    @staticmethod
    def remove_emoji(text: str) -> str:
        return re.sub(emoji_regex_compiled, '', text)

    @staticmethod
    def remove_stop_words(text: str, stop_words: list[str]) -> str:
        cleared_words = [word for word in word_tokenize(text) if word.isalpha() and word not in stop_words]
        truncated_text = cleared_words[:MAX_POST_LEN_IN_WORDS]
        return ' '.join(truncated_text)

    @staticmethod
    def remove_punctuation(text: str) -> str:
        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        return text.replace('»', '').replace('«', '')

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        return re.sub(r' +', ' ', text)

    def _init_stop_words(self, stop_words_file_path: str) -> list[str]:
        with open(stop_words_file_path) as stop_words_file:
            return json.load(stop_words_file)
