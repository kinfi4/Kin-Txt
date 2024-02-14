import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from kin_statistics_api.containers import Container
from kin_statistics_api.settings import Settings
from kin_statistics_api import views, constants, events
from kin_statistics_api.domain import use_cases
from kin_statistics_api.views import api_router
from kin_statistics_api.exception_handlers import pydantic_validation_exception_handler


_logger = logging.getLogger(__name__)


def init_containers(settings: Settings):
    container = Container()
    container.config.from_dict(settings.dict())
    container.init_resources()

    container.wire(
        packages=[views, events],
        modules=[use_cases]
    )

    return container


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts.split(","),
        allow_headers=['*'],
        allow_methods=['*'],
        allow_credentials=True
    )


def create_app(*args, **kwargs):
    settings = Settings()
    app = FastAPI(
        title=constants.PROJECT_TITLE,
        description=constants.PROJECT_DESCRIPTION,
        debug=settings.debug,
    )

    app.include_router(router=api_router)
    app.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)

    container = init_containers(settings)

    init_cors(app, settings)

    app.container = container

    return app


def run_consumer():
    settings = Settings()
    container = init_containers(settings)
    container.check_dependencies()

    _logger.info('Consuming started...')
    container.messaging.subscriber().start_consuming()
