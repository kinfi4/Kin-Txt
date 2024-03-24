import logging

from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError

from kin_statistics_api.domain.entities import User, UserLoginEntity, BaseReport
from kin_statistics_api.exceptions import UsernameAlreadyTakenError
from kin_txt_core.database import Database

from kin_statistics_api.infrastructure.models import User


class IAMRepository:
    def __init__(self, db: Database):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    def get_user(self, username: str) -> UserLoginEntity | None:
        self._logger.info("[UserRepository] Get user from db by username")

        with self._db.session() as session:
            session: Session

            user = session.query(User).get(username)

            if user is None:
                return None

            return UserLoginEntity(username=user.username, password=user.password_hash)

    def create_user(self, username: str, password_hash: str) -> User:
        self._logger.info("[UserRepository] Creating user")

        with self._db.session() as session:
            try:
                user_object = User(username=username, password_hash=password_hash)
                session.add(user_object)
                return User(username=username)
            except IntegrityError:
                raise UsernameAlreadyTakenError(f"User with {username=} already exists, please select another username")

    def get_user_report_ids(self, username: str) -> list[int]:
        with self._db.session() as session:
            session: Session

            user_with_reports = (
                session.query(User)
                .options(selectinload(User.reports))
                .get(username)
            )

        return [report.report_id for report in user_with_reports.reports]

    def update_user_simultaneous_reports_generation(self, username: str, change: int) -> None:
        if change not in [-1, 1]:
            raise ValueError("Change must be -1 or 1")

        with self._db.session() as session:
            session: Session

            user: User = session.query(User).get(username)
            user.simultaneous_reports_generation += change

            self._logger.info(
                f"[UserRepository] User {username=} was increased "
                f"simultaneous_reports_generation to {user.simultaneous_reports_generation}"
            )

    def count_user_reports_synchronous_generations(self, username: str) -> int:
        with self._db.session() as session:
            session: Session

            user: User = session.query(User).get(username)
            return user.simultaneous_reports_generation
