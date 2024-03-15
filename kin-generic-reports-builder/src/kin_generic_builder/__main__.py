import click

from kin_txt_core.messaging.rabbit.dtos import Subscription
from kin_txt_core.reports_building.app import run_consumer

from kin_generic_builder.constants import GENERALE_EXCHANGE
from kin_generic_builder.events.handlers import handle_delete_event
from kin_generic_builder.predictor.factory import KinTxtGenericPredictorFactory
from kin_generic_builder.validation.factory import get_validator_factory
from kin_generic_builder.events import ModelDeleted
from kin_generic_builder.api.server import run_app


@click.group()
def cli():
    pass


@cli.command()
def consume() -> None:
    run_consumer(
        predictor_factory=KinTxtGenericPredictorFactory(),
        validator_factory=get_validator_factory(),
        additional_subscriptions=[
            Subscription(
                callback=handle_delete_event,
                aggregate_type=GENERALE_EXCHANGE,
                event_class=ModelDeleted,
            )
        ],
    )


@cli.command()
def run_server() -> None:
    run_app()


if __name__ == '__main__':
    cli()
