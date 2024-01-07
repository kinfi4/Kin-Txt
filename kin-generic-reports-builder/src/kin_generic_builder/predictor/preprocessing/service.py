import re
import logging
from typing import Iterable
from string import punctuation

import pandas as pd
from nltk.tokenize import word_tokenize
from scipy.sparse.csr import csr_matrix

from kin_generic_builder.predictor.preprocessing.stop_words_loader_mixin import StopWordsLoaderMixin
from kin_txt_core.reports_building.domain.entities import PreprocessingConfig
from kin_txt_core.reports_building.domain.services.predicting.preprocessing import ITextPreprocessor

from kin_generic_builder.predictor.vectorizer.interface import ITextVectorizer
from kin_generic_builder.constants import emoji_regex_compiled


class TextPreprocessor(ITextPreprocessor, ITextVectorizer, StopWordsLoaderMixin):
    def __init__(
        self,
        vectorizer: ITextVectorizer,
        stop_words_storage_path: str | None,
        preprocessing_config: PreprocessingConfig | None = None,
    ) -> None:
        self._vectorizer = vectorizer
        self._stop_words_storage_path = stop_words_storage_path
        self._preprocessing_config = preprocessing_config

        self._logger = logging.getLogger(__name__)

    def preprocess_text(self, text: str) -> str:
        self._reset_current_text_lang()

        if self._preprocessing_config is None:
            return text

        if self._preprocessing_config.lowercase:
            text = text.lower()
        if self._preprocessing_config.remove_links:
            text = self.remove_links(text)
        if self._preprocessing_config.remove_html_tags:
            text = self.remove_html_tags(text)
        if self._preprocessing_config.remove_emoji:
            text = self.remove_emoji(text)
        if self._preprocessing_config.remove_punctuation:
            text = self.remove_punctuation(text)
        if self._preprocessing_config.remove_extra_spaces:
            text = self.remove_extra_spaces(text)
        if self._preprocessing_config.remove_stop_words:
            text = self.remove_stop_words(text)

        return text

    def vectorize(self, texts: Iterable[str], preprocess: bool = False) -> csr_matrix | list:
        if preprocess:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_text)

        return self._vectorizer.vectorize(texts)

    def remove_html_tags(self, text: str) -> str:
        return re.sub(r'<[^>]+>', ' ', text)

    def remove_links(self, text: str) -> str:
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def remove_emoji(self, text: str) -> str:
        return re.sub(emoji_regex_compiled, '', text)

    def remove_stop_words(self, text: str) -> str:
        stop_words_are_valid, stop_words = self.load_stop_words(self._stop_words_storage_path)

        if not stop_words_are_valid:
            self._logger.warning(f"Stop words file {self._stop_words_storage_path} is not valid")
            return text

        cleared_words = [word for word in word_tokenize(text) if word.isalpha() and word not in stop_words]
        return ' '.join(cleared_words)

    def remove_punctuation(self, text: str) -> str:
        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        return text.replace('»', '').replace('«', '')

    def remove_extra_spaces(self, text: str) -> str:
        return re.sub(r' +', ' ', text)

    def _reset_current_text_lang(self) -> None:
        self._current_text_lang = None
