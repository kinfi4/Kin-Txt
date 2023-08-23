from typing import Type, TypeAlias, TypeVar

from dependency_injector import providers, containers, resources
from pymongo import MongoClient

from kin_news_core.messaging import AbstractEventSubscriber, AbstractEventProducer
from kin_news_core.messaging.rabbit import RabbitProducer, RabbitClient, RabbitSubscriber

from kin_model_types.infrastructure.repositories import VisualizationTemplateRepository, ModelRepository
from kin_model_types.constants import MODEL_TYPES_EXCHANGE
from kin_model_types.events.events import ModelValidationFinished, ModelValidationStarted
from kin_model_types.domain.services.model import ModelService


MongoRepositories: TypeAlias = VisualizationTemplateRepository | ModelRepository
TMongoRepository = TypeVar("TMongoRepository", bound=MongoRepositories)


class SubscriberResource(resources.Resource):
    def init(self, client: RabbitClient) -> AbstractEventSubscriber:
        subscriber = RabbitSubscriber(client=client)

        from kin_model_types.events.handlers import (
            on_model_validation_finished,
            on_model_validation_started,
        )

        subscriber.subscribe(MODEL_TYPES_EXCHANGE, ModelValidationFinished, on_model_validation_finished)
        subscriber.subscribe(MODEL_TYPES_EXCHANGE, ModelValidationStarted, on_model_validation_started)

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


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    models_service: providers.Singleton[ModelService] = providers.Singleton(
        ModelService,
        models_storing_path=config.models_storage_path,
        models_repository=repositories.model_repository,
        events_publisher=messaging.producer,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        messaging=messaging,
        repositories=repositories,
    )
