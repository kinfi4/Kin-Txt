import logging

from sqlalchemy import select, insert, func
from sqlalchemy.exc import IntegrityError

from kin_news_api.exceptions import UsernameAlreadyTakenError
from kin_news_core.database import AsyncDatabase
from kin_news_api.infrastructure.models import User, Channel


class UserRepository:
    def __init__(self, db: AsyncDatabase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    async def get_user(self, username: str) -> User | None:
        self._logger.info("[UserRepository] Get user from db by username")

        select_query = (
            select(User)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            user = await session.execute(select_query)
            return user.scalars().one_or_none()

    async def create_user(self, username: str, password: str) -> User:
        self._logger.info("[UserRepository] Creating user")

        insert_query = insert(User).values(username=username, password=password).returning(User)

        async with self._db.session() as session:
            try:
                created_user = await session.execute(insert_query)
                return created_user.scalars()
            except IntegrityError:
                raise UsernameAlreadyTakenError(f"User with {username=} already exists, please select another username")

    async def get_user_subscriptions(self, username: str) -> list[Channel]:
        self._logger.info(f"[UserRepository] Fetching user {username} subscriptions from database")

        select_query = (
            select(Channel)
            .join(Channel.subscribers)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            subscriptions = await session.execute(select_query)
            return subscriptions.scalars().all()

    async def count_user_subscriptions(self, username: str) -> int:
        self._logger.info(f"[UserRepository] Counting user subscriptions for {username}")

        select_query = (
            select(func.count())
            .join(Channel.subscribers)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            result = await session.execute(select_query)

            return result.scalar_one()

    async def check_if_user_fetching_news(self, username: str) -> bool:
        self._logger.info(f"[UserRepository] Checking if user: {username} is already fetching news")

        select_user_query = (
            select(User)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            result = await session.execute(select_user_query)

            return result.scalar().is_fetching

    async def set_user_if_fetching_news(self, username: str, is_fetching: bool) -> None:
        self._logger.info(f"[UserRepository] Setting user: {username} is fetching news to {is_fetching}")

        select_user_query = (
            select(User)
            .where(User.username == username)
        )

        async with self._db.session() as session:
            user = await session.execute(select_user_query)
            user = user.scalar()
            user.is_fetching = is_fetching
