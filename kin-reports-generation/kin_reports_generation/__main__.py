import click

from kin_news_core.reports_building import run_celery, run_consumer
from kin_reports_generation.predictor.factory import KinTxtDefaultPredictorFactory
from kin_reports_generation.validation.factory import get_validator_factory


@click.group()
def cli():
    pass


@cli.command()
def run_tasks():
    run_celery(
        predictor_factory=KinTxtDefaultPredictorFactory(),
        validator_factory=get_validator_factory()
    )


@cli.command()
def consume():
    run_consumer(
        predictor_factory=KinTxtDefaultPredictorFactory(),
        validator_factory=get_validator_factory(),
    )


if __name__ == '__main__':
    cli()
