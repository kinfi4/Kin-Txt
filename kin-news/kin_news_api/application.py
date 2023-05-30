from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kin_news_api import views, constants
from kin_news_api.containers import Container
from kin_news_api.settings import Settings
from kin_news_api.views import api_router
from kin_news_api.views.media import media_router


def init_containers(settings: Settings) -> Container:
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()

    container.wire(packages=[views])

    return container


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_headers=['*'],
        allow_methods=['*'],
        allow_credentials=True
    )


def create_application() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title=constants.PROJECT_TITLE,
        description=constants.PROJECT_DESCRIPTION,
        debug=settings.debug,
    )

    app.include_router(router=api_router)
    app.include_router(router=media_router)

    container = init_containers(settings)

    init_cors(app, settings)

    app.container = container

    return app
