import click

from kin_model_types.run_server import run_app
from kin_model_types.app import run_consumer


@click.group()
def cli():
    pass


@cli.command()
def run_server():
    run_app()


@cli.command()
def consume():
    run_consumer()


if __name__ == '__main__':
    cli()
