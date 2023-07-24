import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kin_reports_generation import Settings, constants
from kin_reports_generation.containers import Container
from kin_reports_generation import events, domain, tasks, views
from kin_reports_generation.views import api_router

_logger = logging.getLogger(__name__)


def init_containers(settings: Settings) -> Container:
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()

    container.wire(
        packages=[domain, events, views],
        modules=[tasks],
    )

    container.check_dependencies()

    return container


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True
    )


def run_celery() -> None:
    settings = Settings()
    _ = init_containers(settings)

    from kin_reports_generation.tasks import celery_app

    celery_app.worker_main(
        ["worker", "-l", "info"]
    )


def run_consumer() -> None:
    settings = Settings()
    container = init_containers(settings)

    _logger.info('Consuming started...')
    container.messaging.subscriber().start_consuming()


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

    app.container = container

    return app
