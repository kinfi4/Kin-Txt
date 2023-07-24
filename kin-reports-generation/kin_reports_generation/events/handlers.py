from typing import Callable, cast

from celery import Task
from kin_news_core.constants import DEFAULT_DATE_FORMAT

from kin_reports_generation.constants import ReportTypes
from kin_reports_generation.domain.events import GenerateReportRequestOccurred
from kin_reports_generation.tasks import generate_word_cloud_task, generate_statistical_report_task


def on_report_processing_request(
    event: GenerateReportRequestOccurred,
) -> None:
    target_task = cast(Task, _get_celery_task_from_event(event))
    target_task.delay(
        start_date=event.start_date.strftime(DEFAULT_DATE_FORMAT),
        end_date=event.end_date.strftime(DEFAULT_DATE_FORMAT),
        channel_list=event.channel_list,
        username=event.username,
        report_id=event.report_id,
        model_id=event.model_id,
        template_id=event.template_id,
    )


def _get_celery_task_from_event(
    event: GenerateReportRequestOccurred
) -> Callable[..., None]:
    if event.report_type == ReportTypes.WORD_CLOUD:
        return generate_word_cloud_task

    if event.report_type == ReportTypes.STATISTICAL:
        return generate_statistical_report_task

    raise RuntimeError('Unknown report type provided!')
