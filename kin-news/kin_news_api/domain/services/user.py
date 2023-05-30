import bcrypt
import logging

from sqlalchemy.exc import NoResultFound

from kin_news_api.domain.entities import UserEntity, UserRegistrationEntity
from kin_news_api.exceptions import LoginFailedError
from kin_news_api.infrastructure.repositories.user import UserRepository
from kin_news_api.settings import Settings
from kin_news_core.auth import create_jwt_token


class UserService:
    def __init__(self, config: Settings, user_repository: UserRepository):
        self._config = config
        self._repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    async def login(self, user_entity: UserEntity) -> str:
        try:
            user = await self._repository.get_user(user_entity.username)
        except NoResultFound:
            raise LoginFailedError("Can not find user with specified username and password")

        if not self._validate_password_hash(user_entity.password, user.password):
            raise LoginFailedError("Can not find user with specified username and password")

        return create_jwt_token(user.username)

    async def register(self, user: UserRegistrationEntity) -> str:
        password_hash = self._hash_password(user.password)

        created_user = await self._repository.create_user(user.username, password_hash)

        return create_jwt_token(created_user.username)

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(password.encode(), salt).decode()

    def _validate_password_hash(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except ValueError:
            return False  # return False if the password hash is invalid
