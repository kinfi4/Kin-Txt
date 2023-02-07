import csv
import tempfile
from typing import Any, Union, IO

from kin_news_core.messaging import AbstractEventProducer
from kin_news_core.constants import DEFAULT_DATE_FORMAT

from kin_reports_generation.domain.entities import GenerateReportEntity, StatisticalReport
from kin_reports_generation.domain.services.interfaces import IGeneratingReportsService
from kin_reports_generation.domain.services.predictor.interfaces import IPredictor
from kin_reports_generation.domain.services.statistical_report.reports_builder import (
    ReportsBuilder,
)
from kin_reports_generation.constants import MessageCategories, SentimentTypes
from kin_news_core.telegram.interfaces import IDataGetterProxy
from kin_reports_generation.infrastructure.services import StatisticsService


class GenerateStatisticalReportService(IGeneratingReportsService):
    reports_builder = ReportsBuilder

    def __init__(
        self,
        telegram_client: IDataGetterProxy,
        predictor: IPredictor,
        events_producer: AbstractEventProducer,
        statistics_service: StatisticsService,
    ) -> None:
        super().__init__(telegram_client, predictor, events_producer)
        self._statistics_service = statistics_service

        self._csv_writer = None

    def _build_report_entity(self, generate_report_entity: GenerateReportEntity) -> StatisticalReport:
        tmp_file = tempfile.NamedTemporaryFile()
        with open(tmp_file.name, 'w') as user_report_file:
            self._csv_writer = csv.writer(user_report_file)
            self._csv_writer.writerow(['date', 'channel', 'hour', 'text', 'sentiment', 'category'])

            report_data = self.__gather_report_data(generate_report_entity)

        with open(tmp_file.name, 'r') as user_report_file:
            self._save_data_to_file(generate_report_entity.report_id, user_report_file)

        return (
            ReportsBuilder.from_report_id(generate_report_entity.report_id)
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

    def _save_data_to_file(self, report_id: int, file: IO) -> None:
        self._statistics_service.save_report_data(report_id=report_id, data=file, file_type='csv')

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
