import click

from kin_news_core.reports_building import run_celery, run_consumer

from kin_news_classification.predictor.factory import KinBertNewsClassificator


@click.group()
def cli():
    pass


@cli.command()
def run_tasks():
    run_celery(predictor_factory=KinBertNewsClassificator())


@cli.command()
def consume():
    run_consumer(predictor_factory=KinBertNewsClassificator())


if __name__ == '__main__':
    cli()
