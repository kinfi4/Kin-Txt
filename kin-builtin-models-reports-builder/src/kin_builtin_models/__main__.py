import click

from kin_txt_core.reports_building.app import run_celery, run_consumer

from kin_builtin_models.predictor.factory import BuiltInModelsPredictorFactory


@click.group()
def cli():
    pass


@cli.command()
def run_tasks():
    run_celery(predictor_factory=BuiltInModelsPredictorFactory())


@cli.command()
def consume():
    run_consumer(predictor_factory=BuiltInModelsPredictorFactory())


if __name__ == '__main__':
    cli()
