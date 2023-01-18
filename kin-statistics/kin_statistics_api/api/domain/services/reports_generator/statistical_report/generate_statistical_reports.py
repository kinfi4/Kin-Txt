import csv
import os
from typing import Any, Union

from api.domain.entities import GenerateReportEntity, StatisticalReport
from api.domain.services.reports_generator.interfaces import IGeneratingReportsService
from api.domain.services.reports_generator.predictor.predictor import Predictor
from api.domain.services.reports_generator.statistical_report.reports_builder import (
    ReportsBuilder,
)
from api.infrastructure.repositories import (
    IReportRepository,
    ReportsAccessManagementRepository,
)
from api.type_hints import CSV_WRITER
from config.constants import DEFAULT_DATE_FORMAT, MessageCategories, SentimentTypes
from kin_news_core.telegram.interfaces import IDataGetterProxy


class GenerateStatisticalReportService(IGeneratingReportsService):
    reports_builder = ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        reports_repository: IReportRepository,
        report_access_repository: ReportsAccessManagementRepository,
        predictor: Predictor,
        reports_folder_path: str,
    ) -> None:
        super().__init__(telegram_client, reports_repository, report_access_repository, predictor)

        self._reports_folder_path = reports_folder_path

        self._csv_writer: CSV_WRITER = None

    def _build_report_entity(self, report_id: int, generate_report_entity: GenerateReportEntity) -> StatisticalReport:
        user_report_file = open(os.path.join(self._reports_folder_path, f'{report_id}.csv'), 'w')
        self._csv_writer = csv.writer(user_report_file)
        self._csv_writer.writerow(['date', 'channel', 'hour', 'text', 'sentiment', 'category'])

        report_data = self.__gather_report_data(generate_report_entity)

        return (
            ReportsBuilder.from_report_id(report_id)
            .set_total_messages_count(report_data['total_messages'])
            .set_messages_count_by_day_hour(report_data['messages_count_by_day_hour'])
            .set_messages_count_by_category(report_data['messages_count_by_category'])
            .set_messages_count_by_channel(report_data['messages_count_by_channel'])
            .set_messages_count_by_date(report_data['messages_count_by_date'])
            .set_messages_count_by_date_by_category(report_data['messages_count_by_date_by_category'])
            .set_messages_count_by_channel_by_category(report_data['messages_count_by_channel_by_category'])
            .set_messages_count_by_sentiment_type(report_data['messages_count_by_sentiment_type'])
            .set_messages_count_by_channel_by_sentiment_type(report_data['messages_count_by_channel_sentiment_type'])
            .set_messages_count_by_date_by_sentiment_type(report_data['messages_count_by_date_by_sentiment_type'])
            .build()
        )

    def __gather_report_data(self, generate_entity: GenerateReportEntity) -> dict[Union[str, MessageCategories], Any]:
        report_data = self._initialize_report_date_dict(generate_entity)

        for channel in generate_entity.channel_list:
            telegram_messages = self._telegram.fetch_posts_from_channel(
                channel_name=channel,
                offset_date=self._datetime_from_date(generate_entity.end_date, end_of_day=True),
                earliest_date=self._datetime_from_date(generate_entity.start_date),
                skip_messages_without_text=True,
            )

            self._logger.info(f'[GenerateStatisticalReportService] Gathered {len(telegram_messages)} messages from {channel}')

            for message in telegram_messages:

                message_date_str = message.created_at.date().strftime(DEFAULT_DATE_FORMAT)
                message_hour = message.created_at.hour

                message_category = self._predictor.get_news_type(message.text)
                message_sentiment_category = self._predictor.get_sentiment_type(
                    message.text,
                    news_type=message_category,
                    make_preprocessing=True,
                )

                self._csv_writer.writerow([
                    message_date_str,
                    channel,
                    message_hour,
                    message.text,
                    message_sentiment_category,
                    message_category,
                ])

                report_data['total_messages'] += 1
                report_data['messages_count_by_channel'][channel] += 1
                report_data['messages_count_by_day_hour'][str(message_hour)] += 1
                report_data['messages_count_by_category'][message_category] += 1
                report_data['message_count_by_sentiment'][message_sentiment_category] += 1

                if message_date_str not in report_data['messages_count_by_date']:
                    report_data['messages_count_by_date'][message_date_str] = 0

                report_data['messages_count_by_date'][message_date_str] += 1

                if message_date_str not in report_data['messages_count_by_date_by_category']:
                    report_data['messages_count_by_date_by_category'][message_date_str] = {
                        category: 0 for category in MessageCategories
                    }

                report_data['messages_count_by_date_by_category'][message_date_str][message_category] += 1

                report_data['messages_count_by_channel_by_category'][channel][message_category] += 1
                report_data['messages_count_by_sentiment_type'][message_sentiment_category] += 1
                report_data['messages_count_by_channel_sentiment_type'][channel][message_sentiment_category] += 1

                if message_date_str not in report_data['messages_count_by_date_by_sentiment_type']:
                    report_data['messages_count_by_date_by_sentiment_type'][message_date_str] = {
                        sentiment_type: 0 for sentiment_type in SentimentTypes
                    }

                report_data['messages_count_by_date_by_sentiment_type'][message_date_str][message_sentiment_category] += 1

        report_data['messages_count_by_date_by_sentiment_type'] = self._reverse_dict_keys(report_data['messages_count_by_date_by_sentiment_type'])
        report_data['messages_count_by_date_by_category'] = self._reverse_dict_keys(report_data['messages_count_by_date_by_category'])
        report_data['messages_count_by_date'] = self._reverse_dict_keys(report_data['messages_count_by_date'])

        return report_data

    @staticmethod
    def _reverse_dict_keys(dct: dict[str, Any]) -> dict[str, Any]:
        dct_reverted_keys = list(dct.keys())[::-1]

        return {
            key: dct[key] for key in dct_reverted_keys
        }

    @staticmethod
    def _initialize_report_date_dict(generate_entity: GenerateReportEntity) -> dict[Union[str, MessageCategories], Any]:
        return {
            'total_messages': 0,
            'messages_count_by_channel': {
                channel: 0 for channel in generate_entity.channel_list
            },
            'messages_count_by_date': {},
            'messages_count_by_day_hour': {
                str(hour): 0 for hour in range(24)
            },
            'messages_count_by_category': {
                category: 0 for category in MessageCategories
            },
            'message_count_by_sentiment': {
                SentimentTypes.NEUTRAL: 0,
                SentimentTypes.POSITIVE: 0,
                SentimentTypes.NEGATIVE: 0,
            },
            'messages_count_by_date_by_category': {},
            'messages_count_by_channel_by_category': {
                channel: {
                    category: 0 for category in MessageCategories
                }
                for channel in generate_entity.channel_list
            },
            'messages_count_by_sentiment_type': {sentiment_type: 0 for sentiment_type in SentimentTypes},
            'messages_count_by_channel_sentiment_type': {
                channel: {
                    sentiment_type: 0 for sentiment_type in SentimentTypes
                }
                for channel in generate_entity.channel_list
            },
            'messages_count_by_date_by_sentiment_type': {},
        }
