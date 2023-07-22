import click

from kin_reports_generation.app import run_celery, run_consumer
from kin_reports_generation.run_server import run_app


@click.group()
def cli():
    pass


@cli.command()
def run_tasks():
    run_celery()


@cli.command()
def consume():
    run_consumer()


@cli.command()
def run_server():
    run_app()


if __name__ == '__main__':
    cli()
