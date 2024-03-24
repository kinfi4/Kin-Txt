from pydantic import Field
from pydantic_settings import BaseSettings

from kin_txt_core.settings import PostgresSettings


class Settings(BaseSettings):
    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(False, validation_alias="DEBUG")
    kin_token: str = Field(..., validation_alias="KIN_TOKEN")

    rabbitmq_connection_string: str = Field(..., validation_alias="RABBITMQ_CONNECTION_STRING")

    allowed_hosts: str = Field(..., validation_alias="ALLOWED_HOSTS")

    database: PostgresSettings = PostgresSettings()
