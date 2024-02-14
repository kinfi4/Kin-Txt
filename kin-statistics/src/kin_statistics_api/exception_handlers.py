from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.requests import Request


def pydantic_validation_exception_handler(_: Request, exc: RequestValidationError) -> Response:
    messages: list[str] = []

    for error in exc.errors():
        if error["type"] == "value_error":
            message: str = error["msg"]
            messages.append(message.replace("Value error, ", ""))
        else:
            messages.append(error["msg"])

    return JSONResponse(
        status_code=422,
        content={"errors": messages},
    )
