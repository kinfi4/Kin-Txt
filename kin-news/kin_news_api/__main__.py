import os

import click
import uvicorn


@click.group()
def cli():
    pass


@cli.command()
def start_app() -> None:
    is_dev_env = bool(int(os.getenv("DEBUG")))
    options = {
        "host": os.environ.get("GUNICORN_HOST", "0.0.0.0"),
        "port": os.environ.get("GUNICORN_PORT", 8000),
        "log_level": "info",
        "workers": 1,
        "reload": is_dev_env,
    }

    uvicorn.run("kin_news_api.application:create_application", **options)


if __name__ == "__main__":
    cli()
