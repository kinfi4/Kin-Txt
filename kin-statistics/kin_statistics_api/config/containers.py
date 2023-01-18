from dependency_injector import containers, providers, resources
from pymongo import MongoClient

from api.domain.services.reports_generator.predictor.predictor import Predictor
from api.infrastructure.repositories import (
    ReportsMongoRepository,
    IReportRepository,
    ReportsAccessManagementRepository,
    UserRepository,
)
from api.domain.services import (
    ManagingReportsService,
    IGeneratingReportsService,
    GenerateStatisticalReportService,
    UserService,
    file_generator_user_case,
    IReportFileGenerator,
    GenerateWordCloudReportService,
)
from kin_news_core.telegram import TelegramClientProxy


class PredictorResource(resources.Resource):
    def init(
        self,
        sentiment_dictionary_path: str,
        sklearn_vectorizer_path: str,
        keras_tokenizer_path: str,
        knn_model_path: str,
        svc_model_path: str,
        gaussian_model_path: str,
        lstm_model_path: str,
    ) -> Predictor:
        return Predictor.create_from_files(
            sentiment_dictionary_path=sentiment_dictionary_path,
            sklearn_vectorizer_path=sklearn_vectorizer_path,
            keras_tokenizer_path=keras_tokenizer_path,
            knn_model_path=knn_model_path,
            gaussian_model_path=gaussian_model_path,
            svc_model_path=svc_model_path,
            lstm_model_path=lstm_model_path
        )


class MongodbRepositoryResource(resources.Resource):
    def init(self, connection_string: str) -> ReportsMongoRepository:
        client = MongoClient(connection_string)

        return ReportsMongoRepository(mongo_client=client)


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()

    reports_repository: providers.Resource[IReportRepository] = providers.Resource(
        MongodbRepositoryResource,
        connection_string=config.MONGO_DB_CONNECTION_STRING,
    )

    reports_access_management_repository: providers.Singleton[ReportsAccessManagementRepository] = providers.Singleton(
        ReportsAccessManagementRepository,
    )

    user_repository: providers.Singleton[UserRepository] = providers.Singleton(
        UserRepository,
    )


class Predicting(containers.DeclarativeContainer):
    config = providers.Configuration()

    predictor: providers.Resource[PredictorResource] = providers.Resource(
        PredictorResource,
        sentiment_dictionary_path=config.SENTIMENT_DICTIONARY_PATH,
        sklearn_vectorizer_path=config.SKLEARN_VECTORIZER_PATH,
        keras_tokenizer_path=config.KERAS_TOKENIZER_PATH,
        knn_model_path=config.KNN_MODEL_PATH,
        gaussian_model_path=config.GAUSSIAN_MODEL_PATH,
        svc_model_path=config.SVC_MODEL_PATH,
        lstm_model_path=config.LSTM_MODEL_PATH,
    )


class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()

    telegram_client: providers.Factory[TelegramClientProxy] = providers.Factory(
        TelegramClientProxy,
        session_str=config.TELEGRAM_SESSION_STRING,
        api_id=config.TELEGRAM_API_ID,
        api_hash=config.TELEGRAM_API_HASH,
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
        reports_folder_path=config.USER_REPORTS_FOLDER_PATH,
    )

    generating_word_cloud_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GenerateWordCloudReportService,
        telegram_client=clients.telegram_client,
        reports_repository=repositories.reports_repository,
        report_access_repository=repositories.reports_access_management_repository,
        predictor=predicting.predictor,
        reports_folder_path=config.USER_REPORTS_FOLDER_PATH,
    )

    user_service: providers.Singleton[UserService] = providers.Singleton(
        UserService,
        access_repository=repositories.user_repository,
    )


class UseCases(containers.DeclarativeContainer):
    config = providers.Configuration()

    report_data_use_case: providers.Callable[..., IReportFileGenerator] = providers.Callable(
        lambda: file_generator_user_case,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
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
