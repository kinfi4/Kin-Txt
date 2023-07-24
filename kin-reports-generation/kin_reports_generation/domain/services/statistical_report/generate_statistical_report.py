import csv
import tempfile
from typing import Any, TextIO

from kin_news_core.messaging import AbstractEventProducer
from kin_news_core.constants import DEFAULT_DATE_FORMAT

from kin_reports_generation.domain.entities import GenerateReportEntity, StatisticalReport, GenerationTemplateWrapper
from kin_reports_generation.domain.services.interfaces import IGeneratingReportsService
from kin_reports_generation.domain.services.predicting import IPredictor

from kin_reports_generation.domain.services.statistical_report.reports_builder import (
    ReportsBuilder,
)
from kin_reports_generation.constants import RawContentTypes
from kin_news_core.telegram.interfaces import IDataGetterProxy
from kin_reports_generation.infrastructure.repositories import ModelRepository, VisualizationTemplateRepository
from kin_reports_generation.infrastructure.services import StatisticsService


class GenerateStatisticalReportService(IGeneratingReportsService):
    reports_builder = ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        events_producer: AbstractEventProducer,
        models_repository: ModelRepository,
        statistics_service: StatisticsService,
        visualization_template_repository: VisualizationTemplateRepository,
    ) -> None:
        super().__init__(telegram_client, events_producer, models_repository, visualization_template_repository)
        self._statistics_service = statistics_service

        self._csv_writer = None

    def _build_report_entity(self, generate_report_entity: GenerationTemplateWrapper) -> StatisticalReport:
        tmp_file = tempfile.NamedTemporaryFile()
        with open(tmp_file.name, "w") as user_report_file:
            self._csv_writer = csv.writer(user_report_file)
            self._csv_writer.writerow(["date", "channel", "hour", "text", "category"])

            report_data = self.__gather_report_data(generate_report_entity)

        with open(tmp_file.name, "r") as user_report_file:
            self._save_data_to_file(generate_report_entity.generate_report_metadata.report_id, user_report_file)

        builder = ReportsBuilder(
            report_id=generate_report_entity.generate_report_metadata.report_id,
            posts_categories=[category for category in generate_report_entity.model_metadata.category_mapping.values()],
            visualization_diagrams_list=generate_report_entity.visualization_template.visualization_diagram_types,
        )

        return (
            builder
            .set_total_messages_count(report_data["total_messages"])
            .set_data(report_data["data"])
            .build()
        )

    def __gather_report_data(self, generate_report_wrapper: GenerationTemplateWrapper) -> dict[str | RawContentTypes, Any]:
        generate_report_meta = generate_report_wrapper.generate_report_metadata
        predictor = generate_report_wrapper.predictor
        posts_category_list = list(generate_report_wrapper.model_metadata.category_mapping.keys())

        report_data = self._initialize_report_data_dict(generate_report_meta)

        for channel in generate_report_meta.channel_list:
            telegram_messages = self._telegram.fetch_posts_from_channel(
                channel_name=channel,
                offset_date=self._datetime_from_date(generate_report_meta.end_date, end_of_day=True),
                earliest_date=self._datetime_from_date(generate_report_meta.start_date),
                skip_messages_without_text=True,
            )

            self._logger.info(f"[GenerateStatisticalReportService] Gathered {len(telegram_messages)} messages from {channel}")

            for message in telegram_messages:
                message_date_str = message.created_at.date().strftime(DEFAULT_DATE_FORMAT)
                message_hour = message.created_at.hour

                message_category = predictor.get_category(message.text)

                self._csv_writer.writerow([
                    message_date_str,
                    channel,
                    message_hour,
                    message.text,
                    message_category,
                ])

                report_data["total_messages"] += 1

                for content_type in generate_report_wrapper.visualization_template.content_types:
                    if content_type == RawContentTypes.BY_CHANNEL:
                        report_data[content_type][channel] += 1
                    elif content_type == RawContentTypes.BY_CATEGORY:
                        report_data[content_type][message_category] += 1
                    elif content_type == RawContentTypes.BY_CHANNEL_BY_CATEGORY:
                        report_data[content_type][channel][message_category] += 1
                    elif content_type == RawContentTypes.BY_DAY_HOUR:
                        report_data[content_type][str(message_hour)] += 1
                    elif content_type == RawContentTypes.BY_DATE:
                        if message_date_str not in report_data[content_type]:
                            report_data[content_type][message_date_str] = 0

                        report_data[content_type][message_date_str] += 1
                    elif content_type == RawContentTypes.BY_DATE_BY_CATEGORY:
                        if message_date_str not in report_data[content_type]:
                            report_data[content_type][message_date_str] = {message_category: 0 for message_category in posts_category_list}

                        report_data[content_type][message_date_str][message_category] += 1
                    elif content_type == RawContentTypes.BY_DATE_BY_CHANNEL:
                        if message_date_str not in report_data[content_type]:
                            report_data[content_type][message_date_str] = {_channel: 0 for _channel in generate_report_meta.channel_list}

                        report_data[content_type][message_date_str][message_category] += 1

        if RawContentTypes.BY_DATE_BY_CHANNEL in generate_report_wrapper.visualization_template.content_types:
            report_data[RawContentTypes.BY_DATE_BY_CHANNEL] = self._reverse_dict_keys(
                report_data[RawContentTypes.BY_DATE_BY_CHANNEL]
            )
        if RawContentTypes.BY_DATE_BY_CATEGORY in generate_report_wrapper.visualization_template.content_types:
            report_data[RawContentTypes.BY_DATE_BY_CATEGORY] = self._reverse_dict_keys(
                report_data[RawContentTypes.BY_DATE_BY_CATEGORY]
            )
        if RawContentTypes.BY_DATE in generate_report_wrapper.visualization_template.content_types:
            report_data[RawContentTypes.BY_DATE] = self._reverse_dict_keys(
                report_data[RawContentTypes.BY_DATE]
            )

        return report_data

    def _save_data_to_file(self, report_id: int, file: TextIO) -> None:
        self._statistics_service.save_report_data(report_id=report_id, data=file, file_type="csv")

    def _reverse_dict_keys(self, dct: dict[str, Any]) -> dict[str, Any]:
        dct_reverted_keys = list(dct.keys())[::-1]

        return {
            key: dct[key] for key in dct_reverted_keys
        }

    def _initialize_report_data_dict(self, generate_report_meta: GenerateReportEntity) -> dict[str | RawContentTypes, Any]:
        _report_data = {}

        for diagram_type in generate_report_meta.set_of_visualization_diagrams:
            _report_data[diagram_type] = self._initialize_diagram_type(diagram_type, generate_report_meta)

        return {
            "total_messages": 0,
            **_report_data,
        }

    def _initialize_diagram_type(self, diagram_type: RawContentTypes, generation_entity: GenerateReportEntity) -> dict[str, Any]:
        if diagram_type == RawContentTypes.BY_CHANNEL:
            return {channel: 0 for channel in generation_entity.channel_list}
        if diagram_type == RawContentTypes.BY_CATEGORY:
            return {category: 0 for category in generation_entity.posts_categories}
        if diagram_type == RawContentTypes.BY_CHANNEL_BY_CATEGORY:
            return {
                channel: {
                    category: 0 for category in generation_entity.posts_categories
                }
                for channel in generation_entity.channel_list
            }
        if diagram_type == RawContentTypes.BY_DAY_HOUR:
            return {str(hour): 0 for hour in range(24)}

        return {}
