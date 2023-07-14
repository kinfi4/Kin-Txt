import click

from .validate import Validator


@click.group()
def cli() -> None:
    pass


@cli.command()
@cli.command("--file-path", "-f", help="Path to file with posts")
@cli.command("--correct-label", "-c", help="Correct label")
def validate_posts(file_path: str, correct_label: str) -> None:
    validator = Validator(file_path, correct_label)

    validator.validate()


if __name__ == "__main__":
    cli()
