from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class PossibleRating(int, Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Channel(models.Model):
    __table_name__ = 'channel'

    link = models.CharField(max_length=255, verbose_name='link', unique=True, null=False, db_index=True)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.link


class ChannelRatings(models.Model):
    __table_name__ = 'channel_rating'

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rate = models.PositiveSmallIntegerField(choices=[(case.value, str(case.value)) for case in PossibleRating], null=True)

    class Meta:
        unique_together = [['user', 'channel']]

    def __str__(self):
        return f'{self.channel.link} - {self.user.username} | rate={self.rate}'


class UserFetchingNews(models.Model):
    __table_name__ = 'user_news_is_fetching'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fetching = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user.username} is fetching news: {self.is_fetching}'
