from dependency_injector import containers, providers, resources
from pymongo import MongoClient

from kin_statistics_api.domain.services.reports_generator.word_cloud.generate_word_cloud_report import (
    GenerateWordCloudReportService,
)
from kin_statistics_api.domain.services.reports_generator.statistical_report.generate_statistical_reports import (
    GenerateStatisticalReportService,
)
from kin_statistics_api.domain.services.reports_generator.interfaces import IGeneratingReportsService
from kin_statistics_api.domain.services.reports_generator.predictor.interfaces import IPredictor
from kin_statistics_api.domain.services.reports_generator.predictor.predictor import Predictor
from kin_statistics_api.infrastructure.repositories import (
    ReportsMongoRepository,
    IReportRepository,
    ReportsAccessManagementRepository,
)
from kin_statistics_api.domain.services import (
    ManagingReportsService,
    UserService,
    CsvFileGenerator,
    JsonFileGenerator,
)
from kin_news_core.telegram import TelegramClientProxy
from kin_news_core.database import Database


class PredictorResource(resources.Resource):
    def init(
        self,
        sentiment_dictionary_path: str,
        stop_words_file_path: str,
        sklearn_vectorizer_path: str,
        knn_model_path: str,
        svc_model_path: str,
        gaussian_model_path: str,
    ) -> IPredictor:
        return Predictor.create_from_files(
            sentiment_dictionary_path=sentiment_dictionary_path,
            stop_words_file_path=stop_words_file_path,
            sklearn_vectorizer_path=sklearn_vectorizer_path,
            knn_model_path=knn_model_path,
            gaussian_model_path=gaussian_model_path,
            svc_model_path=svc_model_path,
        )


class MongodbRepositoryResource(resources.Resource):
    def init(self, connection_string: str) -> ReportsMongoRepository:
        client = MongoClient(connection_string)

        return ReportsMongoRepository(mongo_client=client)


class DatabaseResource(resources.Resource):
    def init(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db_name: str,
    ) -> Database:
        return Database(
            host=host,
            port=port,
            user=user,
            password=password,
            database_name=db_name,
        )

    def shutdown(self, resource: Database) -> None:
        resource.close()


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
        connection_string=config.mongodb_connection_string,
    )

    reports_access_management_repository: providers.Singleton[ReportsAccessManagementRepository] = providers.Singleton(
        ReportsAccessManagementRepository,
        db=database.database_driver,
    )


class Predicting(containers.DeclarativeContainer):
    config = providers.Configuration()

    predictor: providers.Resource[PredictorResource] = providers.Resource(
        PredictorResource,
        sentiment_dictionary_path=config.models.sentiment_dict_path,
        sklearn_vectorizer_path=config.models.ml_vectorizer_path,
        knn_model_path=config.models.knn_model_path,
        gaussian_model_path=config.models.gaussian_model_path,
        svc_model_path=config.models.svc_model_path,
        stop_words_file_path=config.models.stop_words_path,
    )


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    telegram_client: providers.Factory[TelegramClientProxy] = providers.Factory(
        TelegramClientProxy,
        session_str=config.telegram.session_string,
        api_id=config.telegram.api_id,
        api_hash=config.telegram.api_hash,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()
    predicting = providers.DependenciesContainer()

    managing_reports_service: providers.Singleton[ManagingReportsService] = providers.Singleton(
        ManagingReportsService,
        reports_repository=repositories.reports_repository,
        reports_access_management_repository=repositories.reports_access_management_repository,
    )

    generating_reports_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GenerateStatisticalReportService,
        telegram_client=clients.telegram_client,
        reports_repository=repositories.reports_repository,
        report_access_repository=repositories.reports_access_management_repository,
        predictor=predicting.predictor,
        reports_folder_path=config.reports_folder_path,
    )

    generating_word_cloud_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GenerateWordCloudReportService,
        telegram_client=clients.telegram_client,
        reports_repository=repositories.reports_repository,
        report_access_repository=repositories.reports_access_management_repository,
        predictor=predicting.predictor,
        reports_folder_path=config.reports_folder_path,
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


class UseCases(containers.DeclarativeContainer):
    config = providers.Configuration()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
        database=database,
    )

    predicting: providers.Container[Predicting] = providers.Container(
        Predicting,
        config=config,
    )

    clients: providers.Container[Clients] = providers.Container(
        Clients,
        config=config,
    )

    use_cases: providers.Container[UseCases] = providers.Container(
        UseCases,
        config=config,
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
        repositories=repositories,
        clients=clients,
        predicting=predicting,
    )
