import re
import logging
from typing import Iterable, Callable
from string import punctuation

import pandas as pd
from nltk.tokenize import word_tokenize
from scipy.sparse.csr import csr_matrix

from kin_txt_core.reports_building.domain.entities import PreprocessingConfig
from kin_txt_core.reports_building.domain.services.predicting.preprocessing import ITextPreprocessor

from kin_generic_builder.predictor.preprocessing.stop_words_loader_mixin import StopWordsLoaderMixin
from kin_generic_builder.predictor.vectorizer.interface import ITextVectorizer
from kin_generic_builder.constants import emoji_regex_compiled
from kin_txt_core.reports_building.domain.services.predicting.preprocessing.lemmatizer import Lemmatizer


class TextPreprocessor(ITextPreprocessor, ITextVectorizer, StopWordsLoaderMixin, Lemmatizer):
    def __init__(
        self,
        vectorizer: ITextVectorizer,
        stop_words_storage_path: str | None,
        preprocessing_config: PreprocessingConfig | None = None,
    ) -> None:
        super().__init__()

        self._vectorizer = vectorizer
        self._stop_words_storage_path = stop_words_storage_path
        self._preprocessing_config = preprocessing_config

        self._logger = logging.getLogger(__name__)

    def preprocess_text(self, text: str) -> str:
        self._reset_current_text_lang()

        if self._preprocessing_config is None:
            return text

        preprocessing_methods: list[Callable[[str, PreprocessingConfig], str]] = [
            self.make_lower,
            self.remove_links,
            self.remove_html_tags,
            self.remove_emoji,
            self.remove_punctuation,
            self.remove_extra_spaces,
            self.remove_stop_words,
            self.lemmatize_text,
        ]

        for method in preprocessing_methods:
            text = method(text, self._preprocessing_config)

        return text

    def vectorize(self, texts: Iterable[str], preprocess: bool = False) -> csr_matrix | list:
        if preprocess:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_text)

        return self._vectorizer.vectorize(texts)

    def make_lower(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.lowercase:
            return text

        return text.lower()

    def remove_html_tags(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_html_tags:
            return text

        return re.sub(r'<[^>]+>', ' ', text)

    def remove_links(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_links:
            return text

        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def remove_emoji(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_emoji:
            return text

        return re.sub(emoji_regex_compiled, '', text)

    def remove_stop_words(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_stop_words:
            return text

        stop_words_are_valid, stop_words = self.load_stop_words(self._stop_words_storage_path)

        if not stop_words_are_valid:
            self._logger.warning(f"Stop words file {self._stop_words_storage_path} is not valid")
            return text

        cleared_words = [word for word in word_tokenize(text) if word.isalpha() and word not in stop_words]
        return ' '.join(cleared_words)

    def remove_punctuation(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_punctuation:
            return text

        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        text = text.replace('»', '').replace('«', '')

        return text

    def remove_extra_spaces(self, text: str, settings: PreprocessingConfig) -> str:
        if not settings.remove_extra_spaces:
            return text

        return re.sub(r' +', ' ', text)

    def _reset_current_text_lang(self) -> None:
        self._current_text_lang = None
