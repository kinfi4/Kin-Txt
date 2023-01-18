import logging

from django.contrib.auth.models import User

from api.models import Channel


class ChannelRepository:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._query = Channel.objects

    def get_channel_by_link(self, channel_link: str) -> Channel:
        self._logger.info('[ChannelRepository] Getting channel from db by link')

        return self._query.get_or_create(link=channel_link)[0]

    def add_channel_subscriber(self, channel: Channel, user: User) -> None:
        self._logger.info('[ChannelRepository] Add subscriber to the channel')

        channel.subscribers.add(user)
        channel.save()

    def unsubscribe_user(self, user: User, channel_link: str) -> None:
        channel = self._query.get(link=channel_link)
        channel.subscribers.remove(user)
        channel.save()

        if channel.subscribers.count() == 0:
            channel.delete()
