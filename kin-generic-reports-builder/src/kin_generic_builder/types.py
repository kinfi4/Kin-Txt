from typing import Protocol, Any

from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

from kin_txt_core.reports_building.domain.entities import ModelEntity

SkLearnSupportedVectorizers = CountVectorizer | TfidfVectorizer | HashingVectorizer


class Validator(Protocol):
    def __init__(self, path: str) -> None:
        ...

    def validate_model(self, model_entity: ModelEntity) -> None:
        ...


class SklearnPredictor(Protocol):
    def predict(self, *args: Any, **kwargs: Any) -> Any:
        ...


class SklearnTokenizer(Protocol):
    def get_feature_names_out(self) -> list[str]:
        ...

    def transform(self, texts: list[str]) -> csr_matrix:
        pass
