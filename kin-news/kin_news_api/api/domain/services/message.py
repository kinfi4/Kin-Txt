import logging
import random
import time
from datetime import datetime

from api.domain.entities import ChannelGetEntity
from api.domain.entities.message import MessageGetEntity
from api.exceptions import UserAlreadyFetchingNews, UserIsNotSubscribed
from api.infrastructure.repositories import UserRepository
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.telegram import IDataGetterProxy


class MessageService:
    def __init__(self, telegram_client: IDataGetterProxy, user_repository: UserRepository):
        self._telegram_client = telegram_client
        self._user_repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_posts(
        self,
        user_id: int,
        user_channels: list[ChannelGetEntity],
        start_time: datetime,
        end_time: datetime,
    ) -> list[MessageGetEntity]:
        if self._user_repository.check_if_user_fetching_news(user_id):
            raise UserAlreadyFetchingNews(
                'You are sending too many requests. We are preparing your news already. Please wait.'
            )

        if len(user_channels) == 0:
            raise UserIsNotSubscribed()

        messages = []
        try:
            self._user_repository.set_user_if_fetching_news(user_id, True)
            for channel in user_channels:
                self._logger.info(f'Fetching messages for {channel.link}')

                try:
                    channel_messages = self._telegram_client.fetch_posts_from_channel(channel.link, offset_date=end_time, earliest_date=start_time)
                except InvalidChannelURLError:
                    continue  # if the channel has changed it's url, we just skip it

                messages.extend([MessageGetEntity.from_tg_entity(c) for c in channel_messages])

                time.sleep(3 * random.random())  # we need it, in order not to flood the Telegram API
        finally:
            self._user_repository.set_user_if_fetching_news(user_id, False)

        self._logger.info(f'Total messages found for period: {start_time}:{end_time} is {len(messages)}')

        return self._sort_messages_by_time(messages)

    @staticmethod
    def _sort_messages_by_time(messages: list[MessageGetEntity]) -> list[MessageGetEntity]:
        return sorted(messages, key=lambda m: m.created_at, reverse=True)
