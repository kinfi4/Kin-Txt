import os

import uvicorn


def run_app() -> None:
    is_dev_env = bool(int(os.getenv("DEBUG", 0)))
    options = {
        "host": os.environ.get("GUNICORN_HOST", "0.0.0.0"),
        "port": os.environ.get("GUNICORN_PORT", 8000),
        "log_level": "info",
        "workers": 1,
        "reload": is_dev_env,
    }

    uvicorn.run("kin_generic_builder.api.application:create_app", **options)  # type: ignore
