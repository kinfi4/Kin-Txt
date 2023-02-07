import click

from kin_reports_generation.app import run_celery, run_consumer


@click.group()
def cli():
    pass


@cli.command()
def run_tasks():
    run_celery()


@cli.command()
def consume():
    run_consumer()


if __name__ == '__main__':
    cli()
