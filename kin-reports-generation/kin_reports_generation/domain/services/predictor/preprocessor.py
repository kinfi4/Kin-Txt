import json
import re
from string import punctuation
from typing import Optional, Iterable

import pandas as pd
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

from kin_reports_generation.domain.services.predictor import ITextPreprocessor
from kin_reports_generation.constants import MAX_POST_LEN_IN_WORDS, emoji_regex_compiled
from kin_reports_generation.domain.services.predictor.interfaces import ITextVectorizer


class TextPreprocessor(ITextPreprocessor, ITextVectorizer):
    def __init__(
        self,
        stop_words_path: str,
        morph: Optional[MorphAnalyzer] = None,
        sklearn_vectorizer: Optional[TfidfVectorizer] = None,
    ) -> None:
        self._morph = morph if morph else MorphAnalyzer()
        self._vectorizer = sklearn_vectorizer if sklearn_vectorizer else TfidfVectorizer()

        self._russian_stop_words = self._initialize_russian_stop_words(stop_words_path)

    @staticmethod
    def _initialize_russian_stop_words(stop_words_file_path: str) -> list[str]:
        with open(stop_words_file_path) as stop_words_file:
            return json.load(stop_words_file)

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

    def ml_vectorizing(self, texts: Iterable[str], make_preprocessing: bool = True):
        if make_preprocessing:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_and_lemmatize)

        return self._vectorizer.transform(texts)

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
