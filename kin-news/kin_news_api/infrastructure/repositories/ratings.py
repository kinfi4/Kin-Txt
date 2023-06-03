import logging

from sqlalchemy import select, func

from kin_news_api.constants import PossibleRating
from kin_news_api.infrastructure.models import User, Channel, ChannelRatings
from kin_news_core.database import AsyncDatabase


class RatingsRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self._db = db

        self._logger = logging.getLogger(self.__class__.__name__)

    async def set_user_ratings(self, username: str, channel_link: str, rate: PossibleRating) -> ChannelRatings:
        self._logger.info(f"User: {username} set rate: {rate.value} for channel: {channel_link}")

        select_channel_query = (
            select(Channel)
            .where(Channel.link == channel_link)
        )

        select_user_query = (
            select(User)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            channel = await session.execute(select_channel_query)
            user = await session.execute(select_user_query)

            channel = channel.scalar()
            user = user.scalar()

            rating_query = select(ChannelRatings).where(
                (ChannelRatings.user_id == user.id) &
                (ChannelRatings.channel_id == channel.id)
            )
            rating_result = await session.execute(rating_query)
            rating = rating_result.scalar_one_or_none()

            if rating is None:
                rating = ChannelRatings(user_id=user.id, channel_id=channel.id)
                session.add(rating)

            rating.rate = rate.value

        return rating

    async def user_rate(self, username: str, channel_link: str) -> int:
        select_rate_query = (
            select(ChannelRatings)
            .join(User, ChannelRatings.user_id == User.id)
            .join(Channel, ChannelRatings.channel_id == Channel.id)
            .where(Channel.link.ilike(channel_link))
            .where(User.username == username)
        )

        async with self._db.session() as session:
            rating = await session.execute(select_rate_query)
            rate = rating.first()

            return rate[0].rate if rate is not None else 0

    async def get_channel_ratings_stats(self, channel_link: str) -> dict[str, float | int]:
        async with self._db.session() as session:
            stats_query = (
                select(
                    func.count().label("total_rates"),
                    func.coalesce(func.avg(ChannelRatings.rate), 0).label("average_rate")
                )
                .join(Channel, ChannelRatings.channel_id == Channel.id)
                .where(Channel.link == channel_link)
            )

            result = await session.execute(stats_query)
            row = result.first()

            return {"total_rates": row.total_rates, "average_rate": row.average_rate}
