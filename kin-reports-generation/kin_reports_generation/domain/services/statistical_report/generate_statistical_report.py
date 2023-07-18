import csv
import tempfile
from typing import Any, TextIO

from kin_news_core.messaging import AbstractEventProducer
from kin_news_core.constants import DEFAULT_DATE_FORMAT

from kin_reports_generation.domain.entities import GenerateReportEntity, StatisticalReport
from kin_reports_generation.domain.services.interfaces import IGeneratingReportsService
from kin_reports_generation.domain.services.predictor.news_category import NewsCategoryPredictor
from kin_reports_generation.domain.services.statistical_report.reports_builder import (
    ReportsBuilder,
)
from kin_reports_generation.constants import VisualizationDiagrams
from kin_news_core.telegram.interfaces import IDataGetterProxy
from kin_reports_generation.infrastructure.services import StatisticsService


class GenerateStatisticalReportService(IGeneratingReportsService):
    reports_builder = ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        predictor: NewsCategoryPredictor,
        events_producer: AbstractEventProducer,
        statistics_service: StatisticsService,
    ) -> None:
        super().__init__(telegram_client, predictor, events_producer)
        self._statistics_service = statistics_service

        self._csv_writer = None

    def _build_report_entity(self, generate_report_entity: GenerateReportEntity) -> StatisticalReport:
        tmp_file = tempfile.NamedTemporaryFile()
        with open(tmp_file.name, "w") as user_report_file:
            self._csv_writer = csv.writer(user_report_file)
            self._csv_writer.writerow(["date", "channel", "hour", "text", "category"])

            report_data = self.__gather_report_data(generate_report_entity)

        with open(tmp_file.name, "r") as user_report_file:
            self._save_data_to_file(generate_report_entity.report_id, user_report_file)

        builder = ReportsBuilder(
            report_id=generate_report_entity.report_id,
            posts_categories=generate_report_entity.posts_categories,
            set_of_diagrams_to_visualize=generate_report_entity.set_of_visualization_diagrams,
        )

        return (
            builder
            .set_total_messages_count(report_data["total_messages"])
            .set_data(report_data["data"])
            .build()
        )

    def __gather_report_data(self, generate_entity: GenerateReportEntity) -> dict[str | VisualizationDiagrams, Any]:
        report_data = self._initialize_report_data_dict(generate_entity)

        for channel in generate_entity.channel_list:
            telegram_messages = self._telegram.fetch_posts_from_channel(
                channel_name=channel,
                offset_date=self._datetime_from_date(generate_entity.end_date, end_of_day=True),
                earliest_date=self._datetime_from_date(generate_entity.start_date),
                skip_messages_without_text=True,
            )

            self._logger.info(f"[GenerateStatisticalReportService] Gathered {len(telegram_messages)} messages from {channel}")

            for message in telegram_messages:
                message_date_str = message.created_at.date().strftime(DEFAULT_DATE_FORMAT)
                message_hour = message.created_at.hour

                message_category = self._predictor.get_category(message.text)

                self._csv_writer.writerow([
                    message_date_str,
                    channel,
                    message_hour,
                    message.text,
                    message_category,
                ])

                report_data["total_messages"] += 1

                for diagram_type in generate_entity.set_of_visualization_diagrams:
                    if diagram_type == VisualizationDiagrams.BY_CHANNEL:
                        report_data[diagram_type][channel] += 1
                    elif diagram_type == VisualizationDiagrams.BY_CATEGORY:
                        report_data[diagram_type][message_category] += 1
                    elif diagram_type == VisualizationDiagrams.BY_CHANNEL_BY_CATEGORY:
                        report_data[diagram_type][channel][message_category] += 1
                    elif diagram_type == VisualizationDiagrams.BY_DAY_HOUR:
                        report_data[diagram_type][str(message_hour)] += 1
                    elif diagram_type == VisualizationDiagrams.BY_DATE:
                        if message_date_str not in report_data[diagram_type]:
                            report_data[diagram_type][message_date_str] = 0

                        report_data[diagram_type][message_date_str] += 1
                    elif diagram_type == VisualizationDiagrams.BY_DATE_BY_CATEGORY:
                        if message_date_str not in report_data[diagram_type]:
                            report_data[diagram_type][message_date_str] = {message_category: 0 for message_category in generate_entity.posts_categories}

                        report_data[diagram_type][message_date_str][message_category] += 1
                    elif diagram_type == VisualizationDiagrams.BY_DATE_BY_CHANNEL:
                        if message_date_str not in report_data[diagram_type]:
                            report_data[diagram_type][message_date_str] = {_channel: 0 for _channel in generate_entity.channel_list}

                        report_data[diagram_type][message_date_str][message_category] += 1

        if VisualizationDiagrams.BY_DATE_BY_CHANNEL in generate_entity.set_of_visualization_diagrams:
            report_data[VisualizationDiagrams.BY_DATE_BY_CHANNEL] = self._reverse_dict_keys(
                report_data[VisualizationDiagrams.BY_DATE_BY_CHANNEL]
            )
        if VisualizationDiagrams.BY_DATE_BY_CATEGORY in generate_entity.set_of_visualization_diagrams:
            report_data[VisualizationDiagrams.BY_DATE_BY_CATEGORY] = self._reverse_dict_keys(
                report_data[VisualizationDiagrams.BY_DATE_BY_CATEGORY]
            )
        if VisualizationDiagrams.BY_DATE in generate_entity.set_of_visualization_diagrams:
            report_data[VisualizationDiagrams.BY_DATE] = self._reverse_dict_keys(
                report_data[VisualizationDiagrams.BY_DATE]
            )

        return report_data

    def _save_data_to_file(self, report_id: int, file: TextIO) -> None:
        self._statistics_service.save_report_data(report_id=report_id, data=file, file_type="csv")

    def _reverse_dict_keys(self, dct: dict[str, Any]) -> dict[str, Any]:
        dct_reverted_keys = list(dct.keys())[::-1]

        return {
            key: dct[key] for key in dct_reverted_keys
        }

    def _initialize_report_data_dict(self, generate_entity: GenerateReportEntity) -> dict[str | VisualizationDiagrams, Any]:
        _report_data = {}

        for diagram_type in generate_entity.set_of_visualization_diagrams:
            _report_data[diagram_type] = self._initialize_diagram_type(diagram_type, generate_entity)

        return {
            "total_messages": 0,
            **_report_data,
        }

    def _initialize_diagram_type(self, diagram_type: VisualizationDiagrams, generation_entity: GenerateReportEntity) -> dict[str, Any]:
        if diagram_type == VisualizationDiagrams.BY_CHANNEL:
            return {channel: 0 for channel in generation_entity.channel_list}
        if diagram_type == VisualizationDiagrams.BY_CATEGORY:
            return {category: 0 for category in generation_entity.posts_categories}
        if diagram_type == VisualizationDiagrams.BY_CHANNEL_BY_CATEGORY:
            return {
                channel: {
                    category: 0 for category in generation_entity.posts_categories
                }
                for channel in generation_entity.channel_list
            }
        if diagram_type == VisualizationDiagrams.BY_DAY_HOUR:
            return {str(hour): 0 for hour in range(24)}

        return {}
