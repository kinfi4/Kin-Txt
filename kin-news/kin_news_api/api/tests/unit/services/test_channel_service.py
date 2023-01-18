from unittest import mock

from django.test import TestCase

from api.domain.entities import ChannelGetEntity, ChannelPostEntity
from api.tests import factories
from api.views import container


class ChannelsServiceTest(TestCase):
    def test__channel_is_exists__true(self):
        telegram_client_mock = mock.MagicMock()
        telegram_client_mock.get_channel.return_value = True

        with container.clients.telegram_client.override(telegram_client_mock):
            result = container.domain_services.channel_service().channel_exists(ChannelPostEntity(link='something'))

        self.assertTrue(result)

    def test__get_user_subscriptions(self):
        telegram_client_mock = mock.MagicMock()
        cache_client_mock = mock.MagicMock()
        user_repository_mock = mock.MagicMock()

        user_channels = [factories.build_orm_channel() for _ in range(5)]
        user_repository_mock.get_user_subscriptions.return_value = user_channels

        cache_client_mock.get_channel_info.return_value = None
        cache_client_mock.get_channel_photo_url.return_value = None

        telegram_channels = [factories.build_telegram_channel_entity() for _ in range(5)]
        telegram_client_mock.get_channel.side_effect = telegram_channels

        channel_db_links = [obj.link for obj in user_channels]

        with (
            container.clients.telegram_client.override(telegram_client_mock)
            and container.clients.cache_client.override(cache_client_mock)
            and container.repositories.user_repository.override(user_repository_mock)
        ):
            response = container.domain_services.channel_service().get_user_channels("user")

        target_telegram_entities = [
            ChannelGetEntity(
                link=obj.link,
                title=obj.title,
                description=obj.description,
                participants_count=obj.participants_count,
                profile_photo_url=f"/media/profile_photos/{db_link}.jpg",
            ) for db_link, obj in zip(channel_db_links, telegram_channels)
        ]

        self.assertListEqual(response, target_telegram_entities)
        self.assertEqual(cache_client_mock.set_channel_info.call_count, 5)
        self.assertEqual(cache_client_mock.set_channel_photo_url.call_count, 5)

    def test__subscribe(self):
        telegram_client_mock = mock.MagicMock()
        cache_client_mock = mock.MagicMock()
        channel_repository_mock = mock.MagicMock()
        users_repository_mock = mock.MagicMock()

        cache_client_mock.get_channel_info.return_value = None
        cache_client_mock.get_channel_photo_url.return_value = None

        orm_channel = factories.build_orm_channel()
        channel_repository_mock.get_channel_by_link.return_value = orm_channel

        telegram_channel = factories.build_telegram_channel_entity()
        telegram_client_mock.get_channel.return_value = telegram_channel

        users_repository_mock.count_user_subscriptions.return_value = 1

        with (
            container.clients.telegram_client.override(telegram_client_mock)
            and container.clients.cache_client.override(cache_client_mock)
            and container.repositories.channel_repository.override(channel_repository_mock)
            and container.repositories.user_repository.override(users_repository_mock)
        ):
            response = container.domain_services.channel_service().subscribe_user("user", ChannelPostEntity(link="something"))

        target_entity = ChannelGetEntity(
            link=telegram_channel.link,
            title=telegram_channel.title,
            description=telegram_channel.description,
            participants_count=telegram_channel.participants_count,
            profile_photo_url=f"/media/profile_photos/{'something'}.jpg",
        )

        self.assertEqual(response, target_entity)
        self.assertEqual(channel_repository_mock.add_channel_subscriber.call_count, 1)

    def test__unsubscribe(self):
        channel_repository_mock = mock.MagicMock()

        with container.repositories.channel_repository.override(channel_repository_mock):
            response = container.domain_services.channel_service().unsubscribe_channel("user", ChannelPostEntity(link="something"))

        self.assertEqual(channel_repository_mock.unsubscribe_user.call_count, 1)
