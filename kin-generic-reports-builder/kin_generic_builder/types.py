from typing import Protocol

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

from kin_news_core.reports_building.domain.entities import ModelEntity

SkLearnSupportedVectorizers = CountVectorizer | TfidfVectorizer | HashingVectorizer


class Validator(Protocol):
    def __init__(self, path: str) -> None:
        ...

    def validate_model(self, model_entity: ModelEntity) -> None:
        ...
