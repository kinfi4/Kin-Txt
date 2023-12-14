from dependency_injector.wiring import Provide, inject

from kin_model_types.containers import Container
from kin_model_types.events.events import ModelValidationFinished, ModelValidationStarted
from kin_model_types.infrastructure.repositories import ModelRepository
from kin_model_types.constants import ModelStatuses


@inject
def on_model_validation_finished(
    event: ModelValidationFinished,
    models_repository: ModelRepository = Provide[Container.repositories.model_repository],
) -> None:
    models_repository.update_model(
        event.code,
        event.username,
        {
            "model_status": ModelStatuses.VALIDATED if event.validation_passed else ModelStatuses.VALIDATION_FAILED,
            "validation_message": event.message,
        },
    )


@inject
def on_model_validation_started(
    event: ModelValidationStarted,
    models_repository: ModelRepository = Provide[Container.repositories.model_repository],
) -> None:
    models_repository.update_model_status(event.code, event.username, ModelStatuses.VALIDATING)
