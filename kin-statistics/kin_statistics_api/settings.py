from pydantic import BaseSettings, Field

from kin_news_core.settings import PostgresSettings


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


class TelegramSettings(BaseSettings):
    api_id: int = Field(..., env='TELEGRAM_API_ID')
    api_hash: str = Field(..., env='TELEGRAM_API_HASH')
    session_string: str = Field(..., env='TELEGRAM_SESSION_STRING')


class Settings(BaseSettings):
    secret_key: str = Field(..., env='SECRET_KEY')
    log_level: str = Field('INFO', env='LOG_LEVEL')
    debug: bool = Field(False, env='DEBUG')
    token_life_minutes: int = Field(..., env='TOKEN_LIFE_MINUTES')
    max_synchronous_reports_generation: int = Field(3, env='MAX_SYNCHRONOUS_REPORTS_GENERATION')
    reports_folder_path: str = Field(..., env='USER_REPORTS_FOLDER_PATH')
    kin_token: str = Field(..., env='KIN_TOKEN')
    max_channel_per_report_count: int = Field(12, env='MAX_SUBSCRIPTIONS_ALLOWED')
    mongodb_connection_string: str = Field(..., env='MONGO_DB_CONNECTION_STRING')
    allowed_hosts: list[str] = Field(..., env='ALLOWED_HOSTS')

    database: PostgresSettings = PostgresSettings()
    models: ModelSettings = ModelSettings()
    celery: CelerySettings = CelerySettings()
    telegram: TelegramSettings = TelegramSettings()
