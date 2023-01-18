import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet

from api.models import Channel, UserFetchingNews


class UserRepository:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user_query = User.objects
        self._channel_query = Channel.objects
        self._user_fetching_query = UserFetchingNews.objects

    def create_user(self, username: str, password: str) -> User:
        self._logger.info('[UserRepository] Creating user')

        return self._user_query.create_user(username=username, password=password)

    def get_user_by_id(self, user_id: int) -> User:
        self._logger.info('[UserRepository] Get user from db by id')

        return self._user_query.get(pk=user_id)

    def get_user_by_username(self, username: str) -> User:
        self._logger.info('[UserRepository] Get user from db by username')

        return self._user_query.get(username=username)

    def check_if_username_exists(self, username: str) -> bool:
        self._logger.info('[UserRepository] Checking if user exists')

        return self._user_query.filter(username=username).exists()

    def get_user_subscriptions(self, user: User) -> QuerySet[Channel]:
        self._logger.info('[UserRepository] Get user subscriptions from db')

        return self._channel_query.filter(subscribers__username=user.username)

    def count_user_subscriptions(self, user: User) -> int:
        return self._channel_query.filter(subscribers__username=user.username).count()

    def check_if_user_fetching_news(self, user_id: int) -> bool:
        self._logger.info('[UserRepository] Checking if user is already fetching news')

        return self._user_fetching_query.get_or_create(user_id=user_id)[0].is_fetching

    def set_user_if_fetching_news(self, user_id: int, is_fetching: bool) -> None:
        self._logger.info(f'[UserRepository] Setting user is fetching news to {is_fetching}')

        user = self._user_query.get_or_create(pk=user_id)[0]
        user.is_fetching = is_fetching
        user.save()
