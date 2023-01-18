import logging
from typing import Any

from django.db.models import Avg, Count, F, Q
from django.db.models.functions import Coalesce

from api.models import Channel, ChannelRatings, PossibleRating, User


class RatingsRepository:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user_query = User.objects
        self._channel_query = Channel.objects
        self._channel_ratings_query = ChannelRatings.objects

    def set_user_ratings(self, user: User, channel_link: str, rate: PossibleRating) -> ChannelRatings:
        channel = self._channel_query.get(link=channel_link)
        channel_ratings_obj = self._channel_ratings_query.get_or_create(user=user, channel=channel)[0]

        channel_ratings_obj.rate = rate.value
        channel_ratings_obj.save(update_fields=['rate'])

        return channel_ratings_obj

    def user_rate(self, user: User, channel_link: str) -> int:
        return self._channel_ratings_query.get(user=user, channel__link=channel_link).rate

    def get_channel_ratings_stats(self, channel_link: str) -> dict[str, Any]:
        return self._channel_ratings_query.aggregate(
            total_rates=Count(1, filter=Q(channel__link=channel_link)),
            average_rate=Coalesce(Avg(F('rate'), filter=Q(channel__link=channel_link)), 0.0),
        )
