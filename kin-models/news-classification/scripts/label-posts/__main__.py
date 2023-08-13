import click

from .label import Validator


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--file-path", "-f", help="Path to file with posts")
def label(file_path: str) -> None:
    validator = Validator(file_path)
    validator.start_labeling()


if __name__ == "__main__":
    cli()
