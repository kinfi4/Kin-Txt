from abc import ABC, abstractmethod

from kin_reports_generation.domain.services.predicting.preprocessing.interface import ITextPreprocessor


class IPredictor(ITextPreprocessor, ABC):
    @abstractmethod
    def get_category(self, text: str) -> str:
        pass