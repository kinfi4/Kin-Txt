import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from api.domain.entities import RatePostEntity, RatingGetEntity
from api.exceptions import ChannelDoesNotExists
from api.infrastructure.repositories import RatingsRepository


class RatingsService:
    def __init__(
        self,
        ratings_repository: RatingsRepository,
    ) -> None:
        self._ratings_repository = ratings_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def rate_channel(self, user: User, rate_entity: RatePostEntity) -> RatingGetEntity:
        try:
            self._ratings_repository.set_user_ratings(
                user,
                channel_link=rate_entity.channel_link,
                rate=rate_entity.rating,
            )
        except ObjectDoesNotExist:
            raise ChannelDoesNotExists(f'The channel with link {rate_entity.channel_link} is unknown to the system')

        rating_stats = self._ratings_repository.get_channel_ratings_stats(rate_entity.channel_link)

        return RatingGetEntity(
            channel_link=rate_entity.channel_link,
            my_rate=rate_entity.rating,
            total_rates=rating_stats['total_rates'],
            average_rating=rating_stats['average_rate'],
        )

    def get_channel_rating_stats(self, user: User, channel_link: str) -> RatingGetEntity:
        try:
            user_rate = self._ratings_repository.user_rate(user, channel_link)
        except ObjectDoesNotExist:
            user_rate = 0

        rating_stats = self._ratings_repository.get_channel_ratings_stats(channel_link)

        return RatingGetEntity(
            channel_link=channel_link,
            my_rate=user_rate,
            total_rates=rating_stats['total_rates'],
            average_rating=rating_stats['average_rate'],
        )
