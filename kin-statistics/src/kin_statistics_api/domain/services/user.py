import bcrypt

from kin_txt_core.auth import create_jwt_token

from kin_statistics_api.domain.entities import UserLoginEntity, UserRegistrationEntity
from kin_statistics_api.exceptions import LoginFailedError
from kin_statistics_api.infrastructure.repositories import IAMRepository


class UserService:
    def __init__(self, iam_repository: IAMRepository):
        self._iam_repository = iam_repository

    def count_user_reports_generations(self, username: str) -> int:
        return self._iam_repository.count_user_reports_synchronous_generations(username=username)

    def login(self, user_entity: UserLoginEntity) -> str:
        if (user := self._iam_repository.get_user(user_entity.username)) is None:
            raise LoginFailedError("Can not find user with specified username and password")

        if not self._validate_password_hash(user_entity.password, user.password):
            raise LoginFailedError("Can not find user with specified username and password")

        return create_jwt_token(user.username)

    def register(self, user: UserRegistrationEntity) -> str:
        password_hash = self._hash_password(user.password)
        created_user = self._iam_repository.create_user(user.username, password_hash)

        return create_jwt_token(created_user.username)

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def _validate_password_hash(password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except ValueError:
            return False  # return False if the password hash is invalid
