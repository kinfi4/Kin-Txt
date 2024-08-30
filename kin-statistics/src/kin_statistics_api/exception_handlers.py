import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.requests import Request

_logger = logging.getLogger(__name__)

VALUE_ERROR_TYPE = "value_error"


def pydantic_validation_exception_handler(_: Request, exc: RequestValidationError) -> Response:
    messages: list[str] = []

    _logger.warning(f"Request validation error: {exc.errors()}")

    for error in exc.errors():
        error_message: str = error["msg"]

        if error["type"] == VALUE_ERROR_TYPE:
            error_message = error_message.replace("Value error, ", "")

        messages.append(error_message)

    return JSONResponse(
        status_code=422,
        content={"errors": messages},
    )
