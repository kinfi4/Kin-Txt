from abc import ABC, abstractmethod

from kin_reports_generation.domain.entities import ModelEntity


class IModelValidation(ABC):
    @abstractmethod
    def validate_model(self, model: ModelEntity) -> None:
        pass
