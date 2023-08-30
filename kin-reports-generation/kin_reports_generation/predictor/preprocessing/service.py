import os
import re
import json
from string import punctuation
from typing import Iterable

import langid
import pandas as pd
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from scipy.sparse.csr import csr_matrix

from kin_news_core.reports_building.domain.services.predicting.preprocessing.interface import ITextPreprocessor

from kin_reports_generation.predictor.vectorizer.interface import ITextVectorizer
from kin_reports_generation.constants import emoji_regex_compiled
from kin_reports_generation.constants import Languages


class TextPreprocessor(ITextPreprocessor, ITextVectorizer):
    def __init__(
        self,
        stop_words_storage_path: str,
        vectorizer: ITextVectorizer,
    ) -> None:
        self._vectorizer = vectorizer
        self._stop_words_storage_path = stop_words_storage_path

        self._lemmatizers_cache: dict[Languages, MorphAnalyzer] = {}
        self._stop_words_cache: dict[Languages, list[str]] = {}

        self._current_text_lang: Languages | None = None

    def preprocess_text(self, text: str) -> str:
        self._reset_current_text_lang()

        text = text.lower()
        text = self.remove_html_tags(text)
        text = self.remove_links(text)
        text = self.remove_emoji(text)
        text = self.remove_punctuation(text)
        text = self.remove_extra_spaces(text)
        text = self.remove_stop_words(text)

        return text

    def preprocess_and_lemmatize(self, text: str) -> str:
        text = self.preprocess_text(text)
        tokens = word_tokenize(text)

        morph = self._get_lemmatizer(lang=self._get_lang(text))

        return " ".join((morph.parse(word)[0].normal_form for word in tokens))

    def vectorize(self, texts: Iterable[str], preprocess: bool = False) -> csr_matrix | list:
        if preprocess:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_and_lemmatize)

        return self._vectorizer.vectorize(texts)

    def remove_html_tags(self, text: str) -> str:
        return re.sub(r'<[^>]+>', ' ', text)

    def remove_links(self, text: str) -> str:
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def remove_emoji(self, text: str) -> str:
        return re.sub(emoji_regex_compiled, '', text)

    def remove_stop_words(self, text: str) -> str:
        stop_words = self._preload_stop_words(lang=self._get_lang(text))

        cleared_words = [word for word in word_tokenize(text) if word.isalpha() and word not in stop_words]
        truncated_text = cleared_words
        return ' '.join(truncated_text)

    def remove_punctuation(self, text: str) -> str:
        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        return text.replace('»', '').replace('«', '')

    def remove_extra_spaces(self, text: str) -> str:
        return re.sub(r' +', ' ', text)

    def _get_lang(self, text: str) -> Languages:
        if self._current_text_lang is None:
            text_lang = langid.classify(text)[0]

            try:
                self._current_text_lang = Languages(text_lang)
            except ValueError:
                self._current_text_lang = Languages.RUSSIAN

        return self._current_text_lang

    def _get_lemmatizer(self, lang: Languages) -> MorphAnalyzer:
        if lang not in self._lemmatizers_cache:
            self._lemmatizers_cache[lang] = MorphAnalyzer(lang=lang.value)

        return self._lemmatizers_cache[lang]

    def _preload_stop_words(self, lang: Languages) -> list[str]:
        if lang not in self._stop_words_cache:
            with open(os.path.join(self._stop_words_storage_path, f"{lang.value}.json"), "r") as stop_words_file:
                self._stop_words_cache[lang] = json.load(stop_words_file)

        return self._stop_words_cache[lang]

    def _reset_current_text_lang(self) -> None:
        self._current_text_lang = None
