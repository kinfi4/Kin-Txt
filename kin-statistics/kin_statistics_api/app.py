from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kin_statistics_api.containers import Container
from kin_statistics_api.settings import Settings
from kin_statistics_api import views, domain, tasks, constants
from kin_statistics_api.views import api_router


def init_containers(settings: Settings):
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()

    container.wire(
        packages=[views, domain],
        modules=[tasks],
    )

    return container


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
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

    container = init_containers(settings)
    container.check_dependencies()

    init_cors(app, settings)

    app.container = container

    return app


def run_celery():
    settings = Settings()
    _ = init_containers(settings)

    from kin_statistics_api.tasks import celery_app

    celery_app.worker_main(
        ["worker", "-l", "info"]
    )
