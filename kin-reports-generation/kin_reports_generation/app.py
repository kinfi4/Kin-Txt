import logging

from kin_reports_generation import Settings
from kin_reports_generation.containers import Container
from kin_reports_generation import events, domain, tasks

_logger = logging.getLogger(__name__)


def init_containers(settings: Settings):
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()

    container.wire(
        packages=[domain, events],
        modules=[tasks],
    )

    return container


def run_celery():
    settings = Settings()
    _ = init_containers(settings)

    from kin_reports_generation.tasks import celery_app

    celery_app.worker_main(
        ["worker", "-l", "info"]
    )


def run_consumer():
    settings = Settings()
    container = init_containers(settings)
    container.check_dependencies()

    _logger.info('Consuming started...')
    container.messaging.subscriber().start_consuming()
