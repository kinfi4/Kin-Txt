import logging

from sqlalchemy.exc import NoResultFound

from domain.entities import RatePostEntity, RatingGetEntity
from exceptions import ChannelDoesNotExists
from infrastructure.repositories import RatingsRepository


class RatingsService:
    def __init__(
        self,
        ratings_repository: RatingsRepository,
    ) -> None:
        self._ratings_repository = ratings_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    async def rate_channel(self, username: str, rate_entity: RatePostEntity) -> RatingGetEntity:
        try:
            await self._ratings_repository.set_user_ratings(
                username,
                channel_link=rate_entity.channel_link,
                rate=rate_entity.rating,
            )
        except NoResultFound:
            raise ChannelDoesNotExists(f"The channel with link {rate_entity.channel_link} is unknown to the system")

        rating_stats = await self._ratings_repository.get_channel_ratings_stats(rate_entity.channel_link)

        return RatingGetEntity(
            channel_link=rate_entity.channel_link,
            my_rate=rate_entity.rating,
            total_rates=rating_stats['total_rates'],
            average_rating=rating_stats['average_rate'],
        )

    async def get_channel_rating_stats(self, username: str, channel_link: str) -> RatingGetEntity:
        try:
            user_rate = await self._ratings_repository.user_rate(username, channel_link)
        except NoResultFound:
            user_rate = 0

        rating_stats = await self._ratings_repository.get_channel_ratings_stats(channel_link)

        return RatingGetEntity(
            channel_link=channel_link,
            my_rate=user_rate,
            total_rates=rating_stats['total_rates'],
            average_rating=rating_stats['average_rate'],
        )
