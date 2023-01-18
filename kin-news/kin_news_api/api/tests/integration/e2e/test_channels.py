from unittest import mock

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import Client, TestCase

import api.tests.factories as fc
from api.models import Channel, User
from api.tests.integration.e2e.urls import APIUrls
from api.views import container
from kin_news_core.auth import create_jwt_token


class ChannelE2ETests(TestCase):
    def setUp(self) -> None:
        self._test_user = User.objects.create_user("test_username", "test_password")

        _token = create_jwt_token("test_username")
        self._client = Client(HTTP_AUTHORIZATION=f'Token {_token}')

        while True:
            try:
                db_channels = [fc.build_orm_channel() for _ in range(2)]
                self._db_channels = Channel.objects.bulk_create(db_channels)
            except IntegrityError:
                pass
            else:
                break

        for ch in self._db_channels:
            ch.subscribers.add(self._test_user)
            ch.save()

    def tearDown(self) -> None:
        Channel.objects.all().delete()
        User.objects.all().delete()

    def test__getting_user_subscriptions(self):
        telegram_mock = mock.MagicMock()
        tg_channels = [fc.build_telegram_channel_entity(ch.link) for ch in self._db_channels]

        telegram_mock.get_channel.side_effect = tg_channels

        with container.clients.telegram_client.override(telegram_mock):
            response = self._client.get(APIUrls.channels_url)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self._test_user.subscriptions.all()))

    def test__user_unsubscribe(self):
        telegram_mock = mock.MagicMock()

        channel_link_to_unsubscribe = self._db_channels[0].link

        with container.clients.telegram_client.override(telegram_mock):
            response = self._client.delete(APIUrls.channel_details_url(channel_link_to_unsubscribe))

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ObjectDoesNotExist):
            Channel.objects.get(link=channel_link_to_unsubscribe)

    def test__subscribe_to_the_channel(self):
        telegram_mock = mock.MagicMock()

        another_user = User.objects.create_user("another-user", "another-user-password")
        token = create_jwt_token("another-user")
        another_user_client = Client(HTTP_AUTHORIZATION=f'Token {token}')

        channel_to_subscribe = self._db_channels[0]
        telegram_mock.get_channel.return_value = fc.build_telegram_channel_entity(channel_to_subscribe.link)

        with container.clients.telegram_client.override(telegram_mock):
            response = another_user_client.post(
                APIUrls.channels_url,
                data={"link": channel_to_subscribe.link},
                content_type="application/json",
            )

        channel_is_saved = Channel.objects.filter(
            link=channel_to_subscribe.link,
            subscribers__username=another_user.username,
        ).exists()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(channel_is_saved)

    def test__channel_exists(self):
        telegram_mock = mock.MagicMock()

        with container.clients.telegram_client.override(telegram_mock):
            response = self._client.get(APIUrls.channel_exists_url("something"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['exists'], True)
