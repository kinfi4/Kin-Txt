from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from kin_generic_builder.settings import Settings
from kin_generic_builder import constants
from kin_generic_builder.api.views import api_router
from kin_generic_builder.api.exception_handlers import pydantic_validation_exception_handler


def init_cors(app: FastAPI, settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts.split(","),  # type: ignore
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
    app.exception_handler(RequestValidationError, pydantic_validation_exception_handler)

    init_cors(app, settings)

    return app
