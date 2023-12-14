import click

from kin_statistics_api.run_server import run_app
from kin_statistics_api.app import run_consumer


@click.group()
def cli():
    pass


@cli.command()
def run_server():
    run_app()


@cli.command()
def run_rabbitmq():
    run_consumer()


if __name__ == '__main__':
    cli()
