from typing import Iterable

from scipy.sparse import csr_matrix

from kin_reports_generation.domain.services.predicting.vectorizer.interface import ITextVectorizer
from kin_reports_generation.types import SkLearnSupportedVectorizers


class SklearnVectorizer(ITextVectorizer):
    def __init__(self, vectorizer: SkLearnSupportedVectorizers) -> None:
        self._vectorizer = vectorizer

    def vectorize(self, texts: Iterable[str]) -> csr_matrix:
        return self._vectorizer.transform(texts)
