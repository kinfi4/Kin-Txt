from typing import Optional

from dependency_injector import containers, providers, resources

from api.domain.services.message import MessageService
from api.domain.services.ratings import RatingsService
from api.infrastructure.clients.statistics_service import StatisticsServiceProxy
from api.infrastructure.repositories import UserRepository, ChannelRepository
from api.domain.services import UserService, ChannelService
from api.infrastructure.repositories.ratings import RatingsRepository
from kin_news_core.telegram.client import TelegramClientProxy
from kin_news_core.cache import RedisCache, AbstractCache


class RedisResource(resources.Resource):
    def init(self, host: str, port: int = 6379, password: Optional[str] = None, **kwargs) -> RedisCache:
        return RedisCache.from_settings(host, port, password, **kwargs)


class Repositories(containers.DeclarativeContainer):
    user_repository: providers.Singleton[UserRepository] = providers.Singleton(UserRepository)
    channel_repository: providers.Singleton[ChannelRepository] = providers.Singleton(ChannelRepository)
    ratings_repository: providers.Singleton[RatingsRepository] = providers.Singleton(RatingsRepository)


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


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    statistics_service_proxy: providers.Singleton[StatisticsServiceProxy] = providers.Singleton(
        StatisticsServiceProxy,
        statistics_service_url=config.STATISTICS_SERVICE_URL,
        kin_token=config.KIN_TOKEN,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()
    services = providers.DependenciesContainer()

    user_service = providers.Singleton(
        UserService,
        user_repository=repositories.user_repository,
        statistics_proxy=services.statistics_service_proxy,
    )

    message_service = providers.Factory(
        MessageService,
        telegram_client=clients.telegram_client,
        user_repository=repositories.user_repository,
    )

    channel_service = providers.Factory(
        ChannelService,
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

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        repositories=repositories,
        clients=clients,
        services=services,
    )
