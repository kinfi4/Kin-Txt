import os
import json
from datetime import datetime

import click

from fetch import fetch_posts
from fetch_config import LoadPostsConfig


def _validate_channels_file_path(file_path: str) -> bool:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print(f"File {file_path} with channels list doesn't exist")
        return False

    extension = file_path.split(".")[-1]
    if extension != "json":
        print(f"File {file_path} is not json file")
        return False

    return True


def _build_config_object(
    channels_file: str,
    start_date: str,
    end_date: str,
    output_file_path: str,
) -> LoadPostsConfig:
    with open(channels_file, "r") as file:
        channels = json.load(file)["channels"]

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
@click.option("--channels-file", "-f", help="Path to json file with channels list")
@click.option("--start-date", "-s", help="Start date in format YYYY-MM-DD")
@click.option("--end-date", "-e", help="End date in format YYYY-MM-DD")
@click.option("--output-file-path", "-o", help="Path to output file")
def fetch_posts(channels_file: str, start_date: str, end_date: str, output_file_path: str) -> None:
    if not _validate_channels_file_path(channels_file):
        return

    config_object = _build_config_object(channels_file, start_date, end_date, output_file_path)

    fetch_posts(config_object)
