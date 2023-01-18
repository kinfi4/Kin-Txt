import json
import os
from collections import Counter
from itertools import chain
from typing import Any

from api.domain.entities import GenerateReportEntity, WordCloudReport
from api.domain.services.reports_generator.interfaces import IGeneratingReportsService
from api.domain.services.reports_generator.predictor.predictor import Predictor
from api.domain.services.reports_generator.word_cloud.reports_builder import (
    WordCloudReportBuilder,
)
from api.infrastructure.interfaces import IReportRepository
from api.infrastructure.repositories import ReportsAccessManagementRepository
from config.constants import MessageCategories, SentimentTypes
from kin_news_core.telegram import IDataGetterProxy


class GenerateWordCloudReportService(IGeneratingReportsService):
    _MAX_MOST_COMMON_WORDS = 450
    reports_builder = WordCloudReportBuilder

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

    def _build_report_entity(self, report_id: int, generate_report_entity: GenerateReportEntity) -> WordCloudReport:
        gathered_results = self.__gather_data(report_id, generate_report_entity)

        return (
            WordCloudReportBuilder.from_report_id(report_id)
            .set_total_words_count(gathered_results['total_words'])
            .set_data_by_category(gathered_results['data_by_category'])
            .set_data_by_channel(gathered_results['data_by_channel'])
            .set_total_words_frequency(gathered_results['total_words_frequency'])
            .set_data_by_channel_by_category(gathered_results['data_by_channel_by_category'])
            .build()
        )

    def __gather_data(self, report_id: int, generate_report_entity: GenerateReportEntity) -> dict[str, Any]:
        _data = self._initialize_data(generate_report_entity.channel_list)

        for channel_name in generate_report_entity.channel_list:
            telegram_messages = self._telegram.fetch_posts_from_channel(
                channel_name=channel_name,
                offset_date=self._datetime_from_date(generate_report_entity.end_date, end_of_day=True),
                earliest_date=self._datetime_from_date(generate_report_entity.start_date),
                skip_messages_without_text=True,
            )

            self._logger.info(f'[GenerateWordCloudReportService] Gathered {len(telegram_messages)} messages from {channel_name}')

            for message in telegram_messages:
                message_text_preprocessed = self._predictor.preprocess_and_lemmatize(message.text)

                news_category = self._predictor.get_news_type(message.text)
                sentiment_type = self._predictor.get_sentiment_type(
                    message_text_preprocessed,
                    news_category,
                    make_preprocessing=False,
                )

                message_words = message_text_preprocessed.split()
                words_counted = Counter(message_words)

                _data['total_words'] += len(message_words)

                _data['total_words_frequency'].update(words_counted)

                _data['data_by_channel'][channel_name].update(words_counted)

                _data['data_by_category'][news_category].update(words_counted)
                _data['data_by_category'][sentiment_type].update(words_counted)

                _data['data_by_channel_by_category'][channel_name][news_category].update(words_counted)
                _data['data_by_channel_by_category'][channel_name][sentiment_type].update(words_counted)

        self._save_word_cloud_data_to_file(report_id, _data)

        return {
            'total_words': _data['total_words'],
            'data_by_channel_by_category': self._truncate_only_most_popular_words(_data['data_by_channel_by_category']),
            'data_by_category': self._truncate_only_most_popular_words(_data['data_by_category']),
            'data_by_channel': self._truncate_only_most_popular_words(_data['data_by_channel']),
            'total_words_frequency': _data['total_words_frequency'].most_common(self._MAX_MOST_COMMON_WORDS),
        }

    def _save_word_cloud_data_to_file(self, report_id: int, _data: dict[str, int]) -> None:
        report_filepath = os.path.join(self._reports_folder_path, f'{report_id}.json')
        with open(report_filepath, 'w') as report_file:
            json.dump(_data, report_file)

    def _truncate_only_most_popular_words(self, data: dict[str, Any]) -> dict[str, Any]:
        result_data: dict[str, Any] = {}

        for key, word_freq in data.items():
            if isinstance(word_freq, Counter):
                result_data[key] = word_freq.most_common(self._MAX_MOST_COMMON_WORDS)
                continue

            result_data[key] = self._truncate_only_most_popular_words(word_freq)

        return result_data

    @staticmethod
    def _initialize_data(channels: list[str]) -> dict[str, Any]:
        return {
            'total_words': 0,
            'total_words_frequency': Counter(),
            'data_by_channel': {
                channel_name: Counter() for channel_name in channels
            },
            'data_by_category': {
                news_category: Counter() for news_category in chain(list(SentimentTypes), list(MessageCategories))
            },
            'data_by_channel_by_category': {
                channel_name: {
                    news_category: Counter() for news_category in chain(list(SentimentTypes), list(MessageCategories))
                } for channel_name in channels
            }
        }
