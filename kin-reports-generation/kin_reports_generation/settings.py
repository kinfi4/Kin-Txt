from pydantic import BaseSettings, Field


class TelegramSettings(BaseSettings):
    api_id: int = Field(..., env='TELEGRAM_API_ID')
    api_hash: str = Field(..., env='TELEGRAM_API_HASH')
    session_string: str = Field(..., env='TELEGRAM_SESSION_STRING')


class ModelSettings(BaseSettings):
    ml_vectorizer_path: str = Field(..., env='SKLEARN_VECTORIZER_PATH')
    knn_model_path: str = Field(..., env='KNN_MODEL_PATH')
    svc_model_path: str = Field(..., env='SVC_MODEL_PATH')
    gaussian_model_path: str = Field(..., env='GAUSSIAN_MODEL_PATH')

    sentiment_dict_path: str = Field(..., env='SENTIMENT_DICTIONARY_PATH')
    stop_words_path: str = Field(..., env='STOP_WORDS_PATH')


class CelerySettings(BaseSettings):
    broker_url: str = Field(..., env='CELERY_BROKER_URL')
    result_backend: str = Field(..., env='CELERY_RESULT_BACKEND')
    accept_content: list[str] = Field(['application/json'], env='CELERY_ACCEPT_CONTENT')
    task_serializer: str = Field('json', env='CELERY_TASK_SERIALIZER')
    result_serializer: str = Field('json', env='CELERY_RESULT_SERIALIZER')


class Settings(BaseSettings):
    secret_key: str = Field(..., env='SECRET_KEY')
    log_level: str = Field('INFO', env='LOG_LEVEL')
    debug: bool = Field(False, env='DEBUG')
    kin_token: str = Field(..., env='KIN_TOKEN')
    statistics_service: str = Field(..., env='STATISTICS_SERVICE_URL')
    rabbitmq_connection_string: str = Field(..., env='RABBITMQ_CONNECTION_STRING')

    celery: CelerySettings = CelerySettings()
    models: ModelSettings = ModelSettings()
    telegram: TelegramSettings = TelegramSettings()
