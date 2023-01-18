from faker import Faker

from api.domain.services.reports_generator.word_cloud.reports_builder import (
    WordCloudReportBuilder,
)
from config.constants import ReportProcessingResult

_faker = Faker()


def build_wordcloud_report(report_id: int):
    return (
        WordCloudReportBuilder.from_report_id(report_id)
        .set_report_name("TEST NAME")
        .set_status(ReportProcessingResult.READY)
        .set_data_by_channel({_faker.word(): [(_faker.word(), 2), (_faker.word(), 3)]})
        .build()
    )
