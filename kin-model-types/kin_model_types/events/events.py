from kin_news_core.messaging.dtos import BasicEvent

from kin_model_types.domain.entities import ModelEntity


class ModelValidationRequestOccurred(BasicEvent, ModelEntity):
    pass


class ModelValidationStarted(BasicEvent):
    code: str
    username: str


class ModelValidationFinished(BasicEvent):
    code: str
    username: str
    validation_passed: bool
    message: str = None
