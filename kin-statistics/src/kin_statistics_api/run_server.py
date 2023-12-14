import os

import uvicorn


def run_app() -> None:
    is_dev_env = bool(int(os.getenv("DEBUG")))
    options = {
        "host": os.environ.get("GUNICORN_HOST", "0.0.0.0"),
        "port": os.environ.get("GUNICORN_PORT", 8000),
        "log_level": "info",
        "workers": 1,
        "reload": is_dev_env,
    }

    uvicorn.run("kin_statistics_api.app:create_app", **options)
