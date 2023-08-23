class BaseValidationError(Exception):
    pass


class UnsupportedClassifierException(BaseValidationError):
    pass


class UnableToLoadModelError(BaseValidationError):
    pass


class UnableToLoadTokenizerError(BaseValidationError):
    pass


class UnsupportedTokenizerException(BaseValidationError):
    pass


class ModelPredictionError(BaseValidationError):
    pass


class ModelUnsupportedPredictionError(ModelPredictionError):
    pass


class UnsupportedModelTypeError(BaseValidationError):
    pass
