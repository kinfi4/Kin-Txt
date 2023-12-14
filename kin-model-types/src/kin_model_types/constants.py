import re
from enum import Enum, EnumMeta
from typing import Type

PROJECT_TITLE = "Kin-Model-Types"
PROJECT_DESCRIPTION = "Kin-Model-Types is a service for storing, managing user models, templates."

REPORTS_BUILDER_EXCHANGE = "ReportsBuilder"
MODEL_TYPES_EXCHANGE = "ModelTypes"
GENERALE_EXCHANGE = "General"


class ModelStatuses(str, Enum):
    VALIDATED = "Validated"
    VALIDATION_FAILED = "ValidationFailed"
    VALIDATING = "Validating"
    CREATED = "Created"


class ModelTypes(str, Enum):
    SKLEARN = "Sklearn Model"
    TENSORFLOW_BERT = "Tensorflow Bert Model"
    KERAS = "Keras Model"
    CUSTOM = "Custom Model"
