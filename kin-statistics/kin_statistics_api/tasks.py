import logging

from celery import Celery
from dependency_injector.wiring import Provide, inject

from kin_statistics_api import CelerySettings
from kin_statistics_api.domain.entities import GenerateReportEntity
from kin_statistics_api.domain.services.reports_generator.interfaces import IGeneratingReportsService
from kin_statistics_api.containers import Container

_logger = logging.getLogger(__name__)


celery_app = Celery('kin_statistics_api')
celery_app.config_from_object(CelerySettings())


@celery_app.task
@inject
def generate_statistical_report_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    username: str,
    generating_reports_service: IGeneratingReportsService = Provide[Container.services.generating_reports_service],
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
    )

    generating_reports_service.generate_report(generate_report_entity, username)


@celery_app.task
@inject
def generate_word_cloud_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    username: str,
    generating_word_cloud_service: IGeneratingReportsService = Provide[Container.services.generating_word_cloud_service],
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
    )

    generating_word_cloud_service.generate_report(generate_report_entity, username)
