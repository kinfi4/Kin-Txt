from pydantic import Field
from pydantic_settings import BaseSettings

from kin_txt_core.settings import PostgresSettings


class Settings(BaseSettings):
    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(False, validation_alias="DEBUG")
    token_life_minutes: int = Field(..., validation_alias="TOKEN_LIFE_MINUTES")
    max_synchronous_reports_generation: int = Field(3, validation_alias="MAX_SYNCHRONOUS_REPORTS_GENERATION")
    reports_folder_path: str = Field(..., validation_alias="USER_REPORTS_FOLDER_PATH")
    kin_token: str = Field(..., validation_alias="KIN_TOKEN")
    max_channel_per_report_count: int = Field(12, validation_alias="MAX_SUBSCRIPTIONS_ALLOWED")
    mongodb_connection_string: str = Field(..., validation_alias="MONGO_DB_CONNECTION_STRING")
    rabbitmq_connection_string: str = Field(..., validation_alias="RABBITMQ_CONNECTION_STRING")
    allowed_hosts: list[str] = Field(..., validation_alias="ALLOWED_HOSTS")

    database: PostgresSettings = PostgresSettings()
