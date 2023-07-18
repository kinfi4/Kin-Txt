from dependency_injector import providers, containers, resources

from kin_news_core.messaging import AbstractEventSubscriber, AbstractEventProducer
from kin_news_core.messaging.rabbit import RabbitProducer, RabbitClient, RabbitSubscriber
from kin_news_core.telegram import TelegramClientProxy
from kin_reports_generation.domain.services.interfaces import IGeneratingReportsService
from kin_reports_generation.domain.services.predictor import IPredictor
from kin_reports_generation.domain.services.predictor.news_category import NewsCategoryPredictor
from kin_reports_generation.domain.services.statistical_report.generate_statistical_report import (
    GenerateStatisticalReportService
)
from kin_reports_generation.domain.services.word_cloud.generate_word_cloud_report import GenerateWordCloudReportService
from kin_reports_generation.infrastructure.services import StatisticsService
from kin_reports_generation.constants import REPORTS_GENERATION_EXCHANGE
from kin_reports_generation.domain.events import GenerateReportRequestOccurred


class SubscriberResource(resources.Resource):
    def init(self, client: RabbitClient) -> AbstractEventSubscriber:
        subscriber = RabbitSubscriber(client=client)

        from kin_reports_generation.events.handlers import (
            on_report_processing_request,
        )

        subscriber.subscribe(REPORTS_GENERATION_EXCHANGE, GenerateReportRequestOccurred, on_report_processing_request)

        return subscriber


class PredictorResource(resources.Resource):
    def init(
        self,
        stop_words_file_path: str,
        sklearn_vectorizer_path: str,
        svc_model_path: str,
    ) -> IPredictor:
        return NewsCategoryPredictor.create_from_files(
            stop_words_file_path=stop_words_file_path,
            sklearn_vectorizer_path=sklearn_vectorizer_path,
            svc_model_path=svc_model_path,
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


class Predicting(containers.DeclarativeContainer):
    config = providers.Configuration()

    predictor: providers.Resource[PredictorResource] = providers.Resource(
        PredictorResource,
        sklearn_vectorizer_path=config.models.ml_vectorizer_path,
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

    statistics_service: providers.Singleton[StatisticsService] = providers.Singleton(
        StatisticsService,
        url=config.statistics_service,
        kin_token=config.kin_token,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    clients = providers.DependenciesContainer()
    predicting = providers.DependenciesContainer()
    services = providers.DependenciesContainer()
    messaging = providers.DependenciesContainer()

    generating_reports_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GenerateStatisticalReportService,
        telegram_client=clients.telegram_client,
        predictor=predicting.predictor,
        statistics_service=services.statistics_service,
        events_producer=messaging.producer,
    )

    generating_word_cloud_service: providers.Factory[IGeneratingReportsService] = providers.Factory(
        GenerateWordCloudReportService,
        telegram_client=clients.telegram_client,
        predictor=predicting.predictor,
        statistics_service=services.statistics_service,
        events_producer=messaging.producer,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
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

    services: providers.Container[Services] = providers.Container(
        Services,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
        predicting=predicting,
        clients=clients,
        services=services,
        messaging=messaging,
    )
