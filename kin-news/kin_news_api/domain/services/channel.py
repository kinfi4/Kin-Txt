import os
import logging

from sqlalchemy.exc import NoResultFound

from kin_news_api.settings import Settings
from kin_news_api.constants import DELETED_CHANNEL_TITLE
from kin_news_api.domain.entities import ChannelGetEntity, ChannelPostEntity
from kin_news_api.exceptions import UserMaxSubscriptionsExceeded
from kin_news_api.infrastructure.repositories.channel import ChannelRepository
from kin_news_api.infrastructure.repositories.user import UserRepository
from kin_news_core.cache import AsyncRedisCache
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.telegram import IDataGetterProxy


class ChannelService:
    def __init__(
        self,
        config: Settings,
        channel_repository: ChannelRepository,
        user_repository: UserRepository,
        telegram_client: IDataGetterProxy,
        cache_client: AsyncRedisCache,
    ) -> None:
        self._config = config
        self._channel_repository = channel_repository
        self._user_repository = user_repository
        self._telegram_client = telegram_client
        self._cache_client = cache_client
        self._logger = logging.getLogger(self.__class__.__name__)

    async def unsubscribe_channel(self, username: str, channel_post_entity: ChannelPostEntity) -> None:
        try:
            await self._channel_repository.unsubscribe_user(channel_post_entity.link, username)
        except NoResultFound:
            pass

    async def subscribe_user(self, username: str, channel_post_entity: ChannelPostEntity) -> ChannelGetEntity:
        if await self._is_user_subscriptions_exceeded(username):
            raise UserMaxSubscriptionsExceeded(f"User: {username} subscriptions exceeded!")

        channel_entity = await self._get_channel_entity(channel_post_entity.link)

        channel = await self._channel_repository.get_channel_by_link(channel_entity.link)
        await self._channel_repository.add_channel_subscriber(channel, username)

        return channel_entity

    async def get_user_channels(self, username: str) -> list[ChannelGetEntity]:
        orm_channels = await self._user_repository.get_user_subscriptions(username)

        channels: list[ChannelGetEntity] = []
        for orm_channel in orm_channels:
            try:
                channel_entity = await self._get_channel_entity(orm_channel.link)
                channels.append(channel_entity)
            except InvalidChannelURLError:  # in this case url of channel has changed, so we have set default values
                channels.append(self._build_deleted_channel_entity(orm_channel.link))

        return channels

    async def channel_exists(self, channel_post_entity: ChannelPostEntity) -> bool:
        try:
            await self._telegram_client.get_channel_async(channel_link=channel_post_entity.link)
        except InvalidChannelURLError:
            return False

        return True

    async def _get_channel_entity(self, channel_link: str) -> ChannelGetEntity:
        channel_entity = await self._cache_client.get_channel_info(channel_link)

        if channel_entity is None:
            channel_entity = await self._telegram_client.get_channel_async(channel_link)
            await self._cache_client.set_channel_info(channel_entity)

        profile_url = await self._get_channel_profile_photo_url(channel_link)
        return ChannelGetEntity(**channel_entity.dict(), profile_photo_url=profile_url)

    async def _get_channel_profile_photo_url(self, channel_link: str) -> str:
        photo_path = await self._cache_client.get_channel_photo_url(channel_link)

        if photo_path is None or not os.path.exists(os.path.join(self._config.media_root, photo_path)):
            photo_path = os.path.join("profile_photos", f"{channel_link}.jpg")
            photo_absolute_path = os.path.join(self._config.media_root, photo_path)

            await self._telegram_client.download_channel_profile_photo_async(channel_link, photo_absolute_path)
            await self._cache_client.set_channel_photo_url(channel_link, photo_path)

        return f'{self._config.media_root}{photo_path}'

    def _build_deleted_channel_entity(self, link: str) -> ChannelGetEntity:
        return ChannelGetEntity(
            link=link,
            title=DELETED_CHANNEL_TITLE,
            description='',
            participants_count='0 K',
            profile_photo_url=f'{self._config.media_root}{os.path.join("profile_photos", "default.jpg")}',
        )

    async def _is_user_subscriptions_exceeded(self, username: str) -> bool:
        return await self._user_repository.count_user_subscriptions(username) >= self._config.max_user_subscriptions_count
