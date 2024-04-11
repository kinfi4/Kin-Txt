from dependency_injector import providers, containers, resources

from kin_txt_core.database import Database
from kin_txt_core.messaging import AbstractEventSubscriber, AbstractEventProducer
from kin_txt_core.messaging.rabbit import RabbitProducer, RabbitClient, RabbitSubscriber
from kin_txt_core.reports_building.events import ReportsBuilderCreated

from kin_model_types.infrastructure.repositories import VisualizationTemplateRepository, ModelRepository
from kin_model_types.constants import MODEL_TYPES_EXCHANGE
from kin_model_types.events.events import ModelValidationFinished, ModelValidationStarted
from kin_model_types.domain.services.model import ModelService


class DatabaseResource(resources.Resource):
    def init(self, host: str, port: int, user: str, password: str, db_name: str) -> Database:
        db = Database(host=host, port=port, user=user, password=password, database_name=db_name)
        self._make_reflection(db)
        return db

    def _make_reflection(self, db_driver: Database) -> None:
        """
        We need this code to say sqlalchemy about "user" table that was created in statistics service.
        Because without that alchemy is not able to understand the relationship between model and user.

        All about reflections: https://docs.sqlalchemy.org/en/20/core/reflection.html
        """
        from sqlalchemy import Table
        from kin_model_types.infrastructure.models.tables import Base

        connection = db_driver.get_db_connection()
        _ = Table("user", Base.metadata, autoload_with=connection, schema='public')

    def shutdown(self, resource: Database) -> None:
        resource.close()


class SubscriberResource(resources.Resource):
    def init(self, client: RabbitClient) -> AbstractEventSubscriber:
        subscriber = RabbitSubscriber(client=client)

        from kin_model_types.events.handlers import (
            on_model_validation_finished,
            on_model_validation_started,
            on_reports_builder_initialization,
        )

        subscriber.subscribe(MODEL_TYPES_EXCHANGE, ModelValidationFinished, on_model_validation_finished)
        subscriber.subscribe(MODEL_TYPES_EXCHANGE, ModelValidationStarted, on_model_validation_started)
        subscriber.subscribe(MODEL_TYPES_EXCHANGE, ReportsBuilderCreated, on_reports_builder_initialization)

        return subscriber


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database_driver: providers.Resource[Database] = providers.Resource(
        DatabaseResource,
        host=config.database.host,
        port=config.database.port,
        db_name=config.database.db_name,
        user=config.database.user,
        password=config.database.password,
    )


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
    database = providers.DependenciesContainer()

    visualization_template_repository: providers.Singleton[VisualizationTemplateRepository] = providers.Singleton(
        VisualizationTemplateRepository,
        db=database.database_driver,
    )

    model_repository: providers.Singleton[ModelRepository] = providers.Singleton(
        ModelRepository,
        db=database.database_driver,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    models_service: providers.Singleton[ModelService] = providers.Singleton(
        ModelService,
        models_repository=repositories.model_repository,
        events_publisher=messaging.producer,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer,
        config=config,
    )

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
        database=database,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        messaging=messaging,
        repositories=repositories,
    )
