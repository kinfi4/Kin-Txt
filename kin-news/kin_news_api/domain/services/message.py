import random
import asyncio
import logging
from datetime import datetime

from kin_news_api.domain.entities import ChannelGetEntity, MessageGetEntity
from kin_news_api.exceptions import UserAlreadyFetchingNews, UserIsNotSubscribed
from kin_news_api.infrastructure.repositories.user import UserRepository
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.telegram import IDataGetterProxy


class MessageService:
    def __init__(self, telegram_client: IDataGetterProxy, user_repository: UserRepository):
        self._telegram_client = telegram_client
        self._user_repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    async def get_user_posts(
        self,
        username: str,
        user_channels: list[ChannelGetEntity],
        start_time: datetime,
        end_time: datetime,
    ) -> list[MessageGetEntity]:
        if await self._user_repository.check_if_user_fetching_news(username):
            raise UserAlreadyFetchingNews(
                "You are sending too many requests. We are preparing your news already. Please wait."
            )

        if len(user_channels) == 0:
            raise UserIsNotSubscribed()

        messages = []
        try:
            await self._user_repository.set_user_if_fetching_news(username, True)

            for channel in user_channels:
                self._logger.info(f"[MessageService] Fetching messages for {channel.link}")

                try:
                    channel_messages = await self._telegram_client.fetch_posts_from_channel_async(
                        channel.link,
                        offset_date=end_time,
                        earliest_date=start_time,
                    )
                except InvalidChannelURLError:
                    continue  # if the channel has changed it's url, we just skip it

                messages.extend([MessageGetEntity.from_tg_entity(c) for c in channel_messages])

                await asyncio.sleep(3 * random.random()) # we need it, in order not to flood the Telegram API
        finally:
            await self._user_repository.set_user_if_fetching_news(username, False)

        self._logger.info(f"Total messages found for period: {start_time}:{end_time} is {len(messages)}")

        return self._sort_messages_by_time(messages)

    @staticmethod
    def _sort_messages_by_time(messages: list[MessageGetEntity]) -> list[MessageGetEntity]:
        return sorted(messages, key=lambda m: m.created_at, reverse=True)
