from typing import Callable

from api.tasks import generate_statistical_report_task, generate_word_cloud_task
from config.constants import ReportTypes


def generate_report_use_case(report_type: ReportTypes) -> Callable[..., None]:
    if report_type == ReportTypes.WORD_CLOUD:
        return generate_word_cloud_task

    if report_type == ReportTypes.STATISTICAL:
        return generate_statistical_report_task

    raise RuntimeError('Unknown report type provided!')
