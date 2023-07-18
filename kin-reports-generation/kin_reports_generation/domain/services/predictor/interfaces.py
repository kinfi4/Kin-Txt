from abc import ABC, abstractmethod

from kin_reports_generation.constants import MessageCategories, SentimentTypes


class IPredictor(ABC):
    @abstractmethod
    def get_category(self, text: str) -> str:
        pass


class ITextPreprocessor(ABC):
    @abstractmethod
    def preprocess_text(self, text: str) -> str:
        pass

    @abstractmethod
    def preprocess_and_lemmatize(self, text: str) -> str:
        pass


class ITextVectorizer(ABC):
    @abstractmethod
    def ml_vectorizing(self, texts, make_preprocessing: bool = True):
        pass
