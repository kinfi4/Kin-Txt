from typing import Type, TypeAlias, TypeVar

from dependency_injector import providers, containers, resources
from pymongo import MongoClient

from kin_news_core.messaging import AbstractEventSubscriber, AbstractEventProducer
from kin_news_core.messaging.rabbit import RabbitProducer, RabbitClient, RabbitSubscriber
from kin_news_core.telegram import TelegramClientProxy
from kin_reports_generation.infrastructure.repositories import VisualizationTemplateRepository, ModelRepository
from kin_reports_generation.infrastructure.services import StatisticsService
from kin_reports_generation.constants import REPORTS_GENERATION_EXCHANGE
from kin_reports_generation.domain.events import GenerateReportRequestOccurred
from kin_reports_generation.domain.services.model import ModelService, ModelValidationService
from kin_reports_generation.domain.services.statistical_report.generate_statistical_report import GenerateStatisticalReportService
from kin_reports_generation.domain.services.word_cloud.generate_word_cloud_report import GenerateWordCloudReportService


MongoRepositories: TypeAlias = VisualizationTemplateRepository | ModelRepository
TMongoRepository = TypeVar("TMongoRepository", bound=MongoRepositories)


class SubscriberResource(resources.Resource):
    def init(self, client: RabbitClient) -> AbstractEventSubscriber:
        subscriber = RabbitSubscriber(client=client)

        from kin_reports_generation.events.handlers import (
            on_report_processing_request,
        )

        subscriber.subscribe(REPORTS_GENERATION_EXCHANGE, GenerateReportRequestOccurred, on_report_processing_request)

        return subscriber


class MongodbRepositoryResource(resources.Resource):
    def init(self, repository_class: Type[TMongoRepository], connection_string: str) -> TMongoRepository:
        client = MongoClient(connection_string)

        return repository_class(mongo_client=client)


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()

    rabbitmq_client: providers.Singleton[RabbitClient] = providers.Singleton(
        RabbitClient,
        connection_string=config.rabbitmq_connection_string,
    )

    producer: providers.Singleton[AbstractEventProducer] = providers.Singleton(
        RabbitProducer,
        client=rabbitmq_client,
    )

    subscriber: providers.Resource[AbstractEventSubscriber] = providers.Resource(
        SubscriberResource,
        client=rabbitmq_client,
    )


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    telegram_client: providers.Factory[TelegramClientProxy] = providers.Factory(
        TelegramClientProxy,
        session_str=config.telegram.session_string,
        api_id=config.telegram.api_id,
        api_hash=config.telegram.api_hash,
    )


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()

    visualization_template_repository: providers.Resource[MongodbRepositoryResource] = providers.Resource(
        MongodbRepositoryResource,
        repository_class=VisualizationTemplateRepository,
        connection_string=config.mongodb_connection_string,
    )

    model_repository: providers.Resource[MongodbRepositoryResource] = providers.Resource(
        MongodbRepositoryResource,
        repository_class=ModelRepository,
        connection_string=config.mongodb_connection_string,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    statistics_service: providers.Singleton[StatisticsService] = providers.Singleton(
        StatisticsService,
        url=config.statistics_service,
        kin_token=config.kin_token,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    clients = providers.DependenciesContainer()
    services = providers.DependenciesContainer()
    messaging = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    model_validation_service: providers.Singleton[ModelValidationService] = providers.Singleton(
        ModelValidationService,
        model_repository=repositories.model_repository,
    )

    models_service: providers.Singleton[ModelService] = providers.Singleton(
        ModelService,
        models_storing_path=config.models_storage_path,
        model_repository=repositories.model_repository,
    )

    generate_statistics_report_service: providers.Singleton[GenerateStatisticalReportService] = providers.Singleton(
        GenerateStatisticalReportService,
        telegram_client=clients.telegram_client,
        events_producer=messaging.producer,
        models_repository=repositories.model_repository,
        statistics_service=services.statistics_service,
        visualization_template_repository=repositories.visualization_template_repository,
    )

    generate_word_cloud_report_service: providers.Singleton[GenerateWordCloudReportService] = providers.Singleton(
        GenerateWordCloudReportService,
        telegram_client=clients.telegram_client,
        events_producer=messaging.producer,
        models_repository=repositories.model_repository,
        statistics_service=services.statistics_service,
        visualization_template_repository=repositories.visualization_template_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        clients=clients,
        services=services,
        messaging=messaging,
        repositories=repositories,
    )
