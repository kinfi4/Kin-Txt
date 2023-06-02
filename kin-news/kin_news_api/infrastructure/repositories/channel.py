import logging

from sqlalchemy import select, insert, delete, and_
from sqlalchemy.exc import NoResultFound, IntegrityError

from kin_news_api.infrastructure.models import Channel, User, UserChannel
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
        )

        try:
            async with self._db.session() as session:
                fetched_channel = await session.execute(select_query)

                return fetched_channel.scalars().one()
        except NoResultFound:
            insert_query = (
                insert(Channel)
                .values(link=channel_link)
                .returning(Channel)
            )

            async with self._db.session() as session:
                inserted_channel = await session.execute(insert_query)

                return inserted_channel.scalars().one()

    async def add_channel_subscriber(self, channel_link: str, username: str) -> None:
        self._logger.info(f"[ChannelRepository] Add subscriber {username} to the channel {channel_link}")

        channel = await self.get_channel_by_link(channel_link)

        user_id_subquery = (
            select(User.id)
            .where(User.username == username)
            .scalar_subquery()
        )

        insert_user_subscription_query = (
            insert(UserChannel)
            .values(channel_id=channel.id, user_id=user_id_subquery)
        )

        async with self._db.session() as session:
            try:
                await session.execute(insert_user_subscription_query)
            except IntegrityError:
                pass

    async def unsubscribe_user(self, channel_link: str, username: str) -> None:
        self._logger.info(f"[ChannelRepository] Unsubscribe user {username} from the channel {channel_link}")

        user_id_subquery = (
            select(User.id)
            .where(User.username == username)
            .scalar_subquery()
        )

        channel_id_subquery = (
            select(Channel.id)
            .where(Channel.link == channel_link)
            .scalar_subquery()
        )

        delete_subscription_query = (
            delete(UserChannel)
            .where(
                and_(
                    UserChannel.user_id == user_id_subquery,
                    UserChannel.channel_id == channel_id_subquery
                )
            )
        )

        async with self._db.session() as session:
            await session.execute(delete_subscription_query)
