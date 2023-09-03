import click

from kin_news_core.messaging.rabbit.dtos import Subscription
from kin_news_core.reports_building import run_celery, run_consumer

from kin_reports_generation.constants import GENERALE_EXCHANGE
from kin_reports_generation.events.handlers import handle_delete_event
from kin_reports_generation.predictor.factory import KinTxtDefaultPredictorFactory
from kin_reports_generation.validation.factory import get_validator_factory
from kin_reports_generation.events import ModelDeleted


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
        additional_subscriptions=[
            Subscription(
                callback=handle_delete_event,
                aggregate_type=GENERALE_EXCHANGE,
                event_class=ModelDeleted,
            )
        ],
    )


if __name__ == '__main__':
    cli()
