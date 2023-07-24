import logging

from celery import Celery
from dependency_injector.wiring import Provide, inject

from kin_reports_generation.settings import CelerySettings
from kin_reports_generation.domain.entities import GenerateReportEntity
from kin_reports_generation.domain.services.interfaces import IGeneratingReportsService
from kin_reports_generation.containers import Container

_logger = logging.getLogger(__name__)


celery_app = Celery('kin_reports_generation')
celery_app.config_from_object(CelerySettings())


@celery_app.task
@inject
def generate_statistical_report_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    username: str,
    report_id: int,
    model_id: str,
    template_id: str,
    generating_reports_service: IGeneratingReportsService = Provide[Container.domain_services.generating_reports_service],
    **kwargs,
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
        report_id=report_id,
        model_id=model_id,
        template_id=template_id,
    )

    generating_reports_service.generate_report(generate_report_entity, username)


@celery_app.task
@inject
def generate_word_cloud_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    username: str,
    report_id: int,
    model_id: str,
    template_id: str,
    generating_word_cloud_service: IGeneratingReportsService = Provide[Container.domain_services.generating_word_cloud_service],
    **kwargs,
) -> None:
    _logger.info('Instantiating generate report entity and running the processing...')

    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
        report_id=report_id,
        model_id=model_id,
        template_id=template_id,
    )

    generating_word_cloud_service.generate_report(generate_report_entity, username)
