import logging

from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound

from infrastructure.models import Channel, User
from kin_news_core.database import AsyncDatabase


class ChannelRepository:
    def __init__(self, db: AsyncDatabase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    async def get_channel_by_link(self, channel_link: str) -> Channel:
        self._logger.info(f"[ChannelRepository] Getting channel {channel_link} from db by link")

        select_query = (
            select(Channel)
            .where(Channel.link == channel_link)
            .one()
        )

        try:
            async with self._db.session() as session:
                return await session.execute(select_query)
        except NoResultFound:
            insert_query = (
                insert(Channel)
                .values(link=channel_link)
                .returning(Channel)
            )

            async with self._db.session() as session:
                return await session.execute(insert_query)

    async def add_channel_subscriber(self, channel_link: str, username: str) -> None:
        self._logger.info(f"[ChannelRepository] Add subscriber {username} to the channel {channel_link}")

        channel = await self.get_channel_by_link(channel_link)

        select_user_query = (
            select(User)
            .where(User.username == username)
            .one()
        )

        async with self._db.session() as session:
            user = await session.execute(select_user_query)

        channel.subscribers.append(user)

    async def unsubscribe_user(self, channel_link: str, username: str) -> None:
        self._logger.info(f"[ChannelRepository] Unsubscribe user {username} from the channel {channel_link}")

        channel = await self.get_channel_by_link(channel_link)

        select_user_query = (
            select(User)
            .where(User.username == username)
            .one()
        )

        async with self._db.session() as session:
            user = await session.execute(select_user_query)

        channel.subscribers.remove(user)
