import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kin_model_types import constants
from kin_model_types.settings import Settings
from kin_model_types.containers import Container
from kin_model_types import views
from kin_model_types.views import api_router
from kin_model_types.events import handlers

_logger = logging.getLogger(__name__)


def init_containers(settings: Settings) -> Container:
    container = Container()
    container.config.from_dict(settings.dict())
    container.init_resources()

    container.wire(
        packages=[views],
        modules=[handlers],
    )

    container.check_dependencies()

    return container


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_headers=['*'],
        allow_methods=['*'],
        allow_credentials=True
    )


def create_app(*args, **kwargs) -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title=constants.PROJECT_TITLE,
        description=constants.PROJECT_DESCRIPTION,
        debug=settings.debug,
    )

    app.include_router(router=api_router)

    container = init_containers(settings)

    init_cors(app, settings)

    app.container = container  # type: ignore

    return app


def run_consumer() -> None:
    settings = Settings()
    container = init_containers(settings)

    _logger.info('Consuming started...')
    container.messaging.subscriber().start_consuming()
