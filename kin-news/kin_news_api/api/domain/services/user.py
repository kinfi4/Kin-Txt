import logging

from django.core.exceptions import ObjectDoesNotExist

from api.domain.entities import UserEntity, UserRegistrationEntity
from api.exceptions import LoginFailedError, UsernameAlreadyTakenError
from api.infrastructure.clients.statistics_service import StatisticsServiceProxy
from api.infrastructure.repositories import UserRepository
from kin_news_core.auth import create_jwt_token
from kin_news_core.exceptions import ServiceProxyError


class UserService:
    def __init__(self, user_repository: UserRepository, statistics_proxy: StatisticsServiceProxy):
        self._repository = user_repository
        self._statistics_service_proxy = statistics_proxy
        self._logger = logging.getLogger(self.__class__.__name__)

    def login(self, user_entity: UserEntity) -> str:
        try:
            user = self._repository.get_user_by_username(user_entity.username)
        except ObjectDoesNotExist:
            raise LoginFailedError('Can not find user with specified username and password')

        if not user.check_password(user_entity.password):
            raise LoginFailedError('Specified password is incorrect!')

        return create_jwt_token(user.username)

    def register(self, user: UserRegistrationEntity) -> str:
        if self._repository.check_if_username_exists(user.username):
            raise UsernameAlreadyTakenError(f'User with {user.username=} already exists, please select another username')

        try:
            self._statistics_service_proxy.send_create_user_request(username=user.username)
        except ServiceProxyError:
            raise UsernameAlreadyTakenError(f'User with {user.username=} already exists, please select another username')

        created_user = self._repository.create_user(user.username, user.password)

        return create_jwt_token(created_user.username)
