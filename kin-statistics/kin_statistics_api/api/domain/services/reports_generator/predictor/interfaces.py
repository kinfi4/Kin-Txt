from abc import ABC, abstractmethod

import numpy as np

from config.constants import MAX_POST_LEN_IN_WORDS, MessageCategories, SentimentTypes


class IPredictor(ABC):
    @abstractmethod
    def preprocess_text(self, text: str) -> str:
        pass

    @abstractmethod
    def preprocess_and_lemmatize(self, text: str) -> str:
        pass

    @abstractmethod
    def get_sentiment_type(self, text: str, news_type: MessageCategories) -> SentimentTypes:
        pass

    @abstractmethod
    def get_news_type(self, text: str) -> MessageCategories:
        pass


class ITextPreprocessor(ABC):
    @abstractmethod
    def preprocess_text(self, text: str) -> str:
        pass

    @abstractmethod
    def preprocess_and_lemmatize(self, text: str) -> str:
        pass

    @abstractmethod
    def ml_vectorizing(self, texts, make_preprocessing: bool = True):
        pass

    @abstractmethod
    def nn_vectorizing(
        self,
        texts,
        make_preprocessing: bool = True,
        max_words_number: int = MAX_POST_LEN_IN_WORDS,
        padding: str = 'pre',
        truncating: str = 'pre',
    ) -> np.ndarray:
        pass


class ISentimentAnalyzer(ABC):
    @abstractmethod
    def define_sentiment_type(self, text: str, text_type: MessageCategories) -> SentimentTypes:
        pass
