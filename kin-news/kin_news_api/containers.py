from typing import Optional

from dependency_injector import containers, providers, resources

from kin_news_api.infrastructure.repositories.channel import ChannelRepository
from kin_news_api.infrastructure.repositories.user import UserRepository
from kin_news_api.infrastructure.repositories.ratings import RatingsRepository
from kin_news_api.domain.services import UserService, ChannelService, RatingsService, MessageService
from kin_news_core.telegram.client import TelegramClientProxy
from kin_news_core.cache import AsyncRedisCache, AbstractCache
from kin_news_core.database import AsyncDatabase


class RedisResource(resources.Resource):
    def init(self, host: str, port: int = 6379, password: Optional[str] = None, **kwargs) -> AbstractCache:
        return AsyncRedisCache.from_settings(host, port, password, **kwargs)


class DatabaseResource(resources.Resource):
    def init(self, host: str, port: int, user: str, password: str, db_name: str) -> AsyncDatabase:
        return AsyncDatabase(host=host, port=port, user=user, password=password, database_name=db_name)

class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database_driver: providers.Resource[AsyncDatabase] = providers.Resource(
        DatabaseResource,
        host=config.database.host,
        port=config.database.port,
        db_name=config.database.db_name,
        user=config.database.user,
        password=config.database.password,
    )


class Repositories(containers.DeclarativeContainer):
    database = providers.DependenciesContainer()

    user_repository: providers.Singleton[UserRepository] = providers.Singleton(
        UserRepository,
        db=database.database_driver,
    )
    channel_repository: providers.Singleton[ChannelRepository] = providers.Singleton(
        ChannelRepository,
        db=database.database_driver,

    )
    ratings_repository: providers.Singleton[RatingsRepository] = providers.Singleton(
        RatingsRepository,
        db=database.database_driver,
    )


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    cache_client: providers.Resource[AbstractCache] = providers.Resource(
        RedisResource,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        photo_db_name=config.REDIS_PHOTO_DB_NAME,
        channel_db_name=config.REDIS_CHANNEL_DB_NAME,
    )

    telegram_client: providers.Factory[TelegramClientProxy] = providers.Factory(
        TelegramClientProxy,
        session_str=config.TELEGRAM_SESSION_STRING,
        api_id=config.TELEGRAM_API_ID,
        api_hash=config.TELEGRAM_API_HASH,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()

    user_service = providers.Singleton(
        UserService,
        config=config,
        user_repository=repositories.user_repository,
    )

    message_service = providers.Factory(
        MessageService,
        telegram_client=clients.telegram_client,
        user_repository=repositories.user_repository,
    )

    channel_service = providers.Factory(
        ChannelService,
        config=config,
        user_repository=repositories.user_repository,
        channel_repository=repositories.channel_repository,
        telegram_client=clients.telegram_client,
        cache_client=clients.cache_client,
    )

    rating_service = providers.Singleton(
        RatingsService,
        ratings_repository=repositories.ratings_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        database=database,
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        repositories=repositories,
        clients=clients,
    )
