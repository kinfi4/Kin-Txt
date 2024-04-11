from dependency_injector.wiring import Provide, inject

from kin_model_types.containers import Container
from kin_model_types.domain.entities import CustomModelRegistrationEntity
from kin_model_types.domain.services.model import ModelService
from kin_model_types.events.events import ModelValidationFinished, ModelValidationStarted
from kin_model_types.exceptions import ModelAlreadyExistsException
from kin_model_types.infrastructure.repositories import ModelRepository
from kin_model_types.constants import ModelStatuses
from kin_txt_core.reports_building.events import ReportsBuilderCreated


@inject
def on_model_validation_finished(
    event: ModelValidationFinished,
    models_repository: ModelRepository = Provide[Container.repositories.model_repository],
) -> None:
    models_repository.update_model_status(
        event.code,
        event.username,
        status=ModelStatuses.VALIDATED if event.validation_passed else ModelStatuses.VALIDATION_FAILED,
        validation_message=event.message,
    )


@inject
def on_model_validation_started(
    event: ModelValidationStarted,
    models_repository: ModelRepository = Provide[Container.repositories.model_repository],
) -> None:
    models_repository.update_model_status(event.code, event.username, ModelStatuses.VALIDATING)


@inject
def on_reports_builder_initialization(
    event: ReportsBuilderCreated,
    models_service: ModelService = Provide[Container.domain_services.models_service],
) -> None:
    try:
        registration_entity = CustomModelRegistrationEntity(**event.dict())

        models_service.register_custom_model(model_entity=registration_entity)
    except ModelAlreadyExistsException:
        pass
