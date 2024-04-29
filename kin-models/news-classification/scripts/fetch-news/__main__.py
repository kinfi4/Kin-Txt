import os
import json
from datetime import datetime, timedelta

import click

from .fetch import fetch
from .fetch_config import LoadPostsConfig


def _validate_channels_file_path(file_path: str) -> bool:
    if not file_path or not os.path.exists(file_path) or not os.path.isfile(file_path):
        print(f"File {file_path} with channels list doesn't exist")
        return False

    extension = file_path.split(".")[-1]
    if extension != "json":
        print(f"File {file_path} is not json file")
        return False

    return True


def _build_config_object(
    channels_file: str,
    start_date: str | None,
    end_date: str | None,
    output_file_path: str,
) -> LoadPostsConfig:
    with open(channels_file, "r") as file:
        channels = json.load(file)["channels"]

    if start_date is None:
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    return LoadPostsConfig(
        start_date=datetime.strptime(start_date, "%Y-%m-%d"),
        end_date=datetime.strptime(end_date, "%Y-%m-%d"),
        channels=channels,
        output_file_path=output_file_path,
    )


@click.group()
def cli():
    pass


@cli.command()
@click.option("--channels-file", "-f", help="Path to json file with channels list", default="./fetch-news/channels.json")
@click.option("--start-date", "-s", help="Start date in format YYYY-MM-DD")
@click.option("--end-date", "-e", help="End date in format YYYY-MM-DD")
@click.argument("output_file_path")
def fetch_posts(output_file_path: str, channels_file: str | None = None, start_date: str | None = None, end_date: str | None = None) -> None:
    if not _validate_channels_file_path(channels_file):
        return

    config_object = _build_config_object(channels_file, start_date, end_date, output_file_path)

    fetch(config_object)


if __name__ == '__main__':
    cli()
