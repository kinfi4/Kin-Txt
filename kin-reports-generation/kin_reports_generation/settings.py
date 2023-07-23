from pydantic import Field, BaseSettings


class TelegramSettings(BaseSettings):
    api_id: int = Field(..., env="TELEGRAM_API_ID")
    api_hash: str = Field(..., env="TELEGRAM_API_HASH")
    session_string: str = Field(..., env="TELEGRAM_SESSION_STRING")


class CelerySettings(BaseSettings):
    broker_url: str = Field(..., env="CELERY_BROKER_URL")
    result_backend: str = Field(..., env="CELERY_RESULT_BACKEND")
    accept_content: list[str] = Field(["application/json"], env="CELERY_ACCEPT_CONTENT")
    task_serializer: str = Field("json", env="CELERY_TASK_SERIALIZER")
    result_serializer: str = Field("json", env="CELERY_RESULT_SERIALIZER")


class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    debug: bool = Field(False, env="DEBUG")
    kin_token: str = Field(..., env="KIN_TOKEN")
    statistics_service: str = Field(..., env="STATISTICS_SERVICE_URL")
    rabbitmq_connection_string: str = Field(..., env="RABBITMQ_CONNECTION_STRING")
    mongodb_connection_string: str = Field(..., env="MONGO_DB_CONNECTION_STRING")
    models_storage_path: str = Field(..., env="MODELS_STORAGE_PATH")
    default_stop_words_path: str = Field(..., env="DEFAULT_STOP_WORDS_PATH")

    celery: CelerySettings = CelerySettings()
    telegram: TelegramSettings = TelegramSettings()
