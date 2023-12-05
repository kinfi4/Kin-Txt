from typing import Iterable
from abc import ABC, abstractmethod

from scipy.sparse import csr_matrix

__all__ = ["ITextVectorizer"]


class ITextVectorizer(ABC):
    @abstractmethod
    def vectorize(self, texts: Iterable[str]) -> csr_matrix | list:
        pass
