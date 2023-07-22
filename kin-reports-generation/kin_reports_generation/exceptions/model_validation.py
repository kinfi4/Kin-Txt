class BaseValidationError(Exception):
    pass


class UnsupportedClassifierException(BaseValidationError):
    def __init__(self, message: str, model_type: str):
        super().__init__(message)
        self.model_type = model_type


class UnableToLoadModelError(BaseValidationError):
    pass


class UnableToLoadTokenizerError(BaseValidationError):
    pass


class UnsupportedTokenizerException(BaseValidationError):
    def __init__(self, message: str, tokenizer_type: str):
        super().__init__(message)
        self.tokenizer_type = tokenizer_type


class ModelPredictionError(BaseValidationError):
    pass


class ModelUnsupportedPredictionError(ModelPredictionError):
    def __init__(self, prediction_type: str):
        super().__init__(f"Model does not support {prediction_type} prediction")
        self.prediction_type = prediction_type

