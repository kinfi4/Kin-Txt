from unittest import mock

from django.test import TestCase

from api.domain.entities import MessageGetEntity
from api.tests.factories import build_telegram_message
from api.views import container


class TestMessageService(TestCase):
    def test__getting_posts(self):
        telegram_messages = [build_telegram_message() for _ in range(10)]

        telegram_client_mock = mock.MagicMock()
        user_repository_mock = mock.MagicMock()

        user_repository_mock.check_if_user_fetching_news.return_value = False
        telegram_client_mock.fetch_posts_from_channel.return_value = telegram_messages

        with(
            container.clients.telegram_client.override(telegram_client_mock)
            and container.repositories.user_repository.override(user_repository_mock)
        ):
            result = container.domain_services.message_service().get_user_posts(
                user_id=1,
                user_channels=[mock.MagicMock()],
                start_time="",
                end_time="",
            )

        sorted_messages = sorted(telegram_messages, key=lambda message: message.created_at, reverse=True)
        messages_entities = [
            MessageGetEntity(link=obj.message_link, created_at=obj.created_at) for obj in sorted_messages
        ]

        self.assertListEqual(result, messages_entities)
