from unittest import mock

from django.test import TestCase

from api.domain.entities import RatingGetEntity
from api.models import ChannelRatings
from api.tests.factories import build_rate_post_entity
from api.views import container


class TestRatingService(TestCase):
    def test__getting_user_rates_unit(self):
        rating_repository_mock = mock.MagicMock()

        rating_repository_mock.user_rate.return_value = 1
        rating_repository_mock.get_channel_ratings_stats.return_value = {"total_rates": 3, "average_rate": 2.2}

        with container.repositories.ratings_repository.override(rating_repository_mock):
            result = container.domain_services.rating_service().get_channel_rating_stats("", "channel_link")

        target = RatingGetEntity(
            channel_link="channel_link",
            my_rate=1,
            total_rates=3,
            average_rating=2.2,
        )

        self.assertEqual(result, target)

    def test__setting_rate_unit(self):
        rating_repository_mock = mock.MagicMock()

        rating_repository_mock.get_channel_ratings_stats.return_value = {"total_rates": 3, "average_rate": 2.2}

        rate_post_entity = build_rate_post_entity()

        with container.repositories.ratings_repository.override(rating_repository_mock):
            result = container.domain_services.rating_service().rate_channel("", rate_post_entity)

        target = RatingGetEntity(
            channel_link=rate_post_entity.channel_link,
            my_rate=rate_post_entity.rating,
            total_rates=3,
            average_rating=2.2,
        )

        self.assertEqual(result, target)
