from django.test import TestCase

from api.domain.entities import RatePostEntity, RatingGetEntity
from api.models import Channel, ChannelRatings, User
from api.views import container


class TestRating(TestCase):
    def setUp(self):
        self._test_user = User.objects.create_user("test", "test")
        self._test_channel = Channel.objects.create(link="something")
        self._user_ratings = ChannelRatings.objects.create(user=self._test_user, rate=3, channel=self._test_channel)

    def test__getting_user_rates(self):
        result = container.domain_services.rating_service().get_channel_rating_stats(self._test_user, self._test_channel.link)
        target = RatingGetEntity(
            channel_link=self._test_channel.link,
            my_rate=3,
            total_rates=1,
            average_rating=3.0,
        )

        self.assertEqual(result, target)

    def test__setting_ratings(self):
        another_user = User.objects.create_user("another", "test")

        rate_post_entity = RatePostEntity(channel_link=self._test_channel.link, rating=4)
        result = container.domain_services.rating_service().rate_channel(another_user, rate_post_entity)

        target = RatingGetEntity(
            channel_link=self._test_channel.link,
            my_rate=4,
            total_rates=2,
            average_rating=3.5,
        )

        self.assertEqual(result, target)
