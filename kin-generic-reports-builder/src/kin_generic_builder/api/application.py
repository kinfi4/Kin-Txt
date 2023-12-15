from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kin_generic_builder.settings import Settings
from kin_generic_builder import constants
from kin_generic_builder.api.views import api_router


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=Settings.allowed_hosts,
        allow_headers=["*"],
        allow_methods=["*"],
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

    init_cors(app, settings)

    return app
