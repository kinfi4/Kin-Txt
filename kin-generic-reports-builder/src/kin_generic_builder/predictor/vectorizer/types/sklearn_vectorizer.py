from typing import Iterable

from scipy.sparse import csr_matrix

from kin_generic_builder.types import SkLearnSupportedVectorizers

from kin_generic_builder.predictor.vectorizer.interface import ITextVectorizer


class SklearnVectorizer(ITextVectorizer):
    def __init__(self, vectorizer: SkLearnSupportedVectorizers) -> None:
        self._vectorizer = vectorizer

    def vectorize(self, texts: Iterable[str]) -> csr_matrix:
        return self._vectorizer.transform(texts)
