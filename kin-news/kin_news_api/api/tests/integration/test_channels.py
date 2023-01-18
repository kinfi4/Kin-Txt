from unittest import mock

from django.conf import settings
from django.test import TestCase

from api.domain.entities import ChannelGetEntity, ChannelPostEntity
from api.models import Channel, User
from api.tests.factories import build_telegram_channel_entity
from api.views import container


class TestChannels(TestCase):
    def setUp(self):
        self._test_user = User.objects.create_user("test", "test")

    def test__subscribe_user(self):
        telegram_mock = mock.MagicMock()
        cache_client_mock = mock.MagicMock()

        cache_client_mock.get_channel_info.return_value = None
        cache_client_mock.get_channel_photo_url.return_value = None

        tg_channel = build_telegram_channel_entity()
        telegram_mock.get_channel.return_value = tg_channel

        with (
            container.clients.telegram_client.override(telegram_mock)
            and container.clients.cache_client.override(cache_client_mock)
        ):
            container.domain_services.channel_service().subscribe_user(self._test_user, ChannelPostEntity(link=tg_channel.link))

        is_channel_created = Channel.objects.filter(link=tg_channel.link).exists()
        self.assertTrue(is_channel_created)

        channel_subscribers = Channel.objects.get(link=tg_channel.link).subscribers.all()
        self.assertIn(self._test_user, channel_subscribers)

    def test__unsubscribe_channel(self):
        test_channel = Channel.objects.create(link="unsubscribe_channel")
        test_channel.subscribers.add(self._test_user)
        test_channel.subscribers.add(User.objects.create_user("test2", "test2"))
        test_channel.save()

        container.domain_services.channel_service().unsubscribe_channel(self._test_user, ChannelPostEntity(link="unsubscribe_channel"))

        self.assertNotIn(self._test_user, Channel.objects.get(link="unsubscribe_channel").subscribers.all())

    def test__getting_user_channels(self):
        cache_client_mock = mock.MagicMock()
        cache_client_mock.get_channel_info.return_value = None
        cache_client_mock.get_channel_photo_url.return_value = None

        telegram_mock = mock.MagicMock()
        tg_channels = [build_telegram_channel_entity() for _ in range(2)]
        telegram_mock.get_channel.side_effect = tg_channels

        channel1 = Channel(link=tg_channels[0].link)
        channel2 = Channel(link=tg_channels[1].link)
        Channel.objects.bulk_create([channel1, channel2])

        channel1.subscribers.add(self._test_user)
        channel1.save()
        channel2.subscribers.add(self._test_user)
        channel2.save()

        with (
            container.clients.telegram_client.override(telegram_mock)
            and container.clients.cache_client.override(cache_client_mock)
        ):
            result = container.domain_services.channel_service().get_user_channels(self._test_user)

        target_list = [
            ChannelGetEntity(
                link=obj.link,
                title=obj.title,
                description=obj.description,
                participants_count=obj.participants_count,
                profile_photo_url=f'{settings.MEDIA_ROOT}/profile_photos/{obj.link}.jpg'
            ) for obj in tg_channels
        ]

        self.assertEqual(len(result), 2)
        self.assertListEqual(target_list, result)
