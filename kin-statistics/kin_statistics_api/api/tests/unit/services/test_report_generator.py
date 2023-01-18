from unittest import mock

from django.test import TestCase

from api.domain.entities import StatisticalReport
from api.tests import factories
from api.views import container
from config.constants import (
    DEFAULT_DATE_FORMAT,
    MessageCategories,
    ReportProcessingResult,
    SentimentTypes,
)


class TestReportGenerationService(TestCase):
    def test__report_generation(self):
        access_repo_mock = mock.MagicMock()
        reports_repo_mock = mock.MagicMock()
        telegram_client_mock = mock.MagicMock()
        predictor_mock = mock.MagicMock()

        access_repo_mock.create_new_user_report.return_value = 1

        messages = [factories.build_telegram_message_entity() for _ in range(100)]
        telegram_client_mock.fetch_posts_from_channel.return_value = messages

        categories = [factories.get_random_message_category() for _ in range(100)]
        predictor_mock.get_news_type.side_effect = categories

        sentiment_types = [factories.get_random_sentiment_type() for _ in range(100)]
        predictor_mock.get_sentiment_type.side_effect = sentiment_types

        target_report = StatisticalReport(
            report_id=1,
            name='',
            processing_status=ReportProcessingResult.READY,
            report_failed_reason=None,
            total_messages_count=100,
            messages_count_by_channel={"ChannelName": 100},
            messages_count_by_date={
                date_str: sum(
                    [1 for message in messages if message.created_at.date().strftime(DEFAULT_DATE_FORMAT) == date_str])
                for date_str in set([message.created_at.date().strftime(DEFAULT_DATE_FORMAT) for message in messages])
            },
            messages_count_by_day_hour={
                str(message_hour): sum([1 for message in messages if message.created_at.hour == message_hour])
                for message_hour in range(24)
            },
            messages_count_by_category={
                category: sum([1 for c in categories if c == category])
                for category in list(MessageCategories)
            },
            messages_count_by_date_by_category={
                date_str: {
                    category: sum([
                        1 for c, message in zip(categories, messages)
                        if message.created_at.date().strftime(DEFAULT_DATE_FORMAT) == date_str
                           and c == category
                    ]) for category in list(MessageCategories)
                } for date_str in set([message.created_at.date().strftime(DEFAULT_DATE_FORMAT) for message in messages])
            },
            messages_count_by_channel_by_category={
                "ChannelName": {
                    category: sum([1 for c in categories if c == category])
                    for category in list(MessageCategories)
                }
            },
            messages_count_by_sentiment_type={
                sentiment: sum([1 for s in sentiment_types if s == sentiment])
                for sentiment in list(SentimentTypes)
            },
            messages_count_by_channel_by_sentiment_type={
                "ChannelName": {
                    sentiment: sum([1 for s in sentiment_types if s == sentiment])
                    for sentiment in list(SentimentTypes)
                }
            },
            messages_count_by_date_by_sentiment_type={
                date_str: {
                    sentiment: sum([
                        1 for s, message in zip(sentiment_types, messages)
                        if message.created_at.date().strftime(DEFAULT_DATE_FORMAT) == date_str
                           and s == sentiment
                    ]) for sentiment in list(SentimentTypes)
                } for date_str in set([message.created_at.date().strftime(DEFAULT_DATE_FORMAT) for message in messages])
            },
        )

        with (
            container.repositories.reports_repository.override(reports_repo_mock)
            and container.repositories.reports_access_management_repository.override(access_repo_mock)
            and container.clients.telegram_client.override(telegram_client_mock)
            and container.predicting.predictor.override(predictor_mock)
        ):
            result: StatisticalReport = container.services.generating_reports_service().generate_report(
                factories.build_generate_report_entity(), 2
            )

        self.assertEqual(result.report_id, target_report.report_id)
        self.assertEqual(result.processing_status, target_report.processing_status)
        self.assertEqual(result.total_messages_count, target_report.total_messages_count)
        self.assertDictEqual(result.messages_count_by_channel, target_report.messages_count_by_channel)
        self.assertDictEqual(result.messages_count_by_date, target_report.messages_count_by_date)
        self.assertDictEqual(result.messages_count_by_day_hour, target_report.messages_count_by_day_hour)
        self.assertDictEqual(result.messages_count_by_category, target_report.messages_count_by_category)
        self.assertDictEqual(result.messages_count_by_date_by_category, target_report.messages_count_by_date_by_category)
        self.assertDictEqual(result.messages_count_by_channel_by_category, target_report.messages_count_by_channel_by_category)
        self.assertDictEqual(result.messages_count_by_sentiment_type, target_report.messages_count_by_sentiment_type)
        self.assertDictEqual(result.messages_count_by_channel_by_sentiment_type, target_report.messages_count_by_channel_by_sentiment_type)
        self.assertDictEqual(result.messages_count_by_date_by_sentiment_type, target_report.messages_count_by_date_by_sentiment_type)
