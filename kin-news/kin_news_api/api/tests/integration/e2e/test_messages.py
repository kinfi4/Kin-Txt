from unittest import mock

from django.db import IntegrityError
from django.test import Client, TestCase

from api.models import Channel, User
from api.tests import factories as fc
from api.tests.integration.e2e.urls import APIUrls
from api.views import container
from kin_news_core.auth import create_jwt_token


class TestMessagesE2E(TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user("some-username", "password")
        token = create_jwt_token(test_user.username)

        self._client = Client(HTTP_AUTHORIZATION=f"Token {token}")

        while True:
            try:
                db_channels = [fc.build_orm_channel() for _ in range(2)]
                self._db_channels = Channel.objects.bulk_create(db_channels)
            except IntegrityError:
                pass
            else:
                break

        for ch in self._db_channels:
            ch.subscribers.add(test_user)
            ch.save()

    def tearDown(self) -> None:
        Channel.objects.all().delete()
        User.objects.all().delete()

    def test__getting_messages(self):
        telegram_mock = mock.MagicMock()
        tg_messages = [fc.build_telegram_message() for _ in range(2)]
        telegram_mock.fetch_posts_from_channel.side_effect = [[tg_messages[0]], [tg_messages[1]]]

        tg_channels = [fc.build_telegram_channel_entity(ch.link) for ch in self._db_channels]
        telegram_mock.get_channel.side_effect = tg_channels

        with container.clients.telegram_client.override(telegram_mock):
            response = self._client.get(APIUrls.messages_url)

            self.assertEqual(response.status_code, 200)
