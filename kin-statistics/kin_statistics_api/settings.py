from pydantic import BaseSettings, Field

from kin_news_core.settings import PostgresSettings


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
    rabbitmq_connection_string: str = Field(..., env='RABBITMQ_CONNECTION_STRING')
    allowed_hosts: list[str] = Field(..., env='ALLOWED_HOSTS')

    database: PostgresSettings = PostgresSettings()
