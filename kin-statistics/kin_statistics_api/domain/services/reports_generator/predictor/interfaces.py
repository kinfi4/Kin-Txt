from abc import ABC, abstractmethod

from kin_statistics_api.constants import MessageCategories, SentimentTypes


class IPredictor(ABC):
    @abstractmethod
    def preprocess_text(self, text: str) -> str:
        pass

    @abstractmethod
    def preprocess_and_lemmatize(self, text: str) -> str:
        pass

    @abstractmethod
    def get_sentiment_type(self, text: str, news_type: MessageCategories, make_preprocessing: bool = False) -> SentimentTypes:
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


class ISentimentAnalyzer(ABC):
    @abstractmethod
    def define_sentiment_type(self, text: str, text_type: MessageCategories) -> SentimentTypes:
        pass
