from typing import Type

from dependency_injector import containers, providers, resources
from pymongo import MongoClient

from kin_statistics_api.domain.services.report_data import ReportDataSaver
from kin_statistics_api.infrastructure.repositories import (
    ReportsMongoRepository,
    IReportRepository,
    ReportsAccessManagementRepository,
    TemplatesRepository,
)
from kin_statistics_api.domain.services import (
    ManagingReportsService,
    UserService,
    CsvFileGenerator,
    JsonFileGenerator,
    GenerationTemplateService,
)
from kin_statistics_api.constants import REPORTS_STORING_EXCHANGE
from kin_news_core.database import Database
from kin_news_core.messaging import AbstractEventSubscriber, AbstractEventProducer
from kin_news_core.messaging.rabbit import RabbitProducer, RabbitClient, RabbitSubscriber


class SubscriberResource(resources.Resource):
    def init(self, client: RabbitClient) -> AbstractEventSubscriber:
        subscriber = RabbitSubscriber(client=client)

        from kin_statistics_api.events.handlers import (
            on_processing_failed,
            on_processing_started,
            on_processing_finished,
        )

        from kin_statistics_api.domain.events import (
            StatisticalReportProcessingFinished,
            WordCloudReportProcessingFinished,
            ReportProcessingFailed,
            ReportProcessingStarted,
        )

        subscriber.subscribe(REPORTS_STORING_EXCHANGE, ReportProcessingStarted, on_processing_started)
        subscriber.subscribe(REPORTS_STORING_EXCHANGE, ReportProcessingFailed, on_processing_failed)
        subscriber.subscribe(REPORTS_STORING_EXCHANGE, WordCloudReportProcessingFinished, on_processing_finished)
        subscriber.subscribe(REPORTS_STORING_EXCHANGE, StatisticalReportProcessingFinished, on_processing_finished)

        return subscriber


class MongodbRepositoryResource(resources.Resource):
    def init(self, repository_class: Type[TemplatesRepository | ReportsMongoRepository], connection_string: str) -> ReportsMongoRepository:
        client = MongoClient(connection_string)

        return repository_class(mongo_client=client)


class DatabaseResource(resources.Resource):
    def init(self, host: str, port: int, user: str, password: str, db_name: str) -> Database:
        return Database(host=host, port=port, user=user, password=password, database_name=db_name)

    def shutdown(self, resource: Database) -> None:
        resource.close()


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


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    database = providers.DependenciesContainer()

    reports_repository: providers.Resource[IReportRepository] = providers.Resource(
        MongodbRepositoryResource,
        repository_class=ReportsMongoRepository,
        connection_string=config.mongodb_connection_string,
    )

    reports_access_management_repository: providers.Singleton[ReportsAccessManagementRepository] = providers.Singleton(
        ReportsAccessManagementRepository,
        db=database.database_driver,
    )

    templates_repository: providers.Resource[TemplatesRepository] = providers.Resource(
        MongodbRepositoryResource,
        repository_class=TemplatesRepository,
        connection_string=config.mongodb_connection_string,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    messaging = providers.DependenciesContainer()

    managing_reports_service: providers.Singleton[ManagingReportsService] = providers.Singleton(
        ManagingReportsService,
        events_producer=messaging.producer,
        reports_repository=repositories.reports_repository,
        reports_access_management_repository=repositories.reports_access_management_repository,
    )

    user_service: providers.Singleton[UserService] = providers.Singleton(
        UserService,
        access_repository=repositories.reports_access_management_repository,
    )

    csv_data_generator: providers.Singleton[CsvFileGenerator] = providers.Singleton(
        CsvFileGenerator,
        access_repository=repositories.reports_access_management_repository,
    )

    json_data_generator: providers.Singleton[JsonFileGenerator] = providers.Singleton(
        JsonFileGenerator,
        access_repository=repositories.reports_access_management_repository,
    )

    reports_data_saver: providers.Singleton[ReportDataSaver] = providers.Singleton(
        ReportDataSaver,
        reports_folder_path=config.reports_folder_path,
    )

    templates_service: providers.Singleton[GenerationTemplateService] = providers.Singleton(
        GenerationTemplateService,
        templates_repository=repositories.templates_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
    )

    database: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
        database=database,
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
        repositories=repositories,
        messaging=messaging,
    )
