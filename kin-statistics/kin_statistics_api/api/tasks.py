import logging

from dependency_injector.wiring import Provide, inject

from api.domain.entities import GenerateReportEntity
from api.domain.services import IGeneratingReportsService
from config.celery import celery_app
from config.containers import Container

_logger = logging.getLogger(__name__)


@celery_app.task
@inject
def generate_statistical_report_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    user_id: int,
    generating_reports_service: IGeneratingReportsService = Provide[Container.services.generating_reports_service],
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
    )

    generating_reports_service.generate_report(generate_report_entity, user_id)


@celery_app.task
@inject
def generate_word_cloud_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    user_id: int,
    generating_word_cloud_service: IGeneratingReportsService = Provide[Container.services.generating_word_cloud_service],
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
    )

    generating_word_cloud_service.generate_report(generate_report_entity, user_id)
