from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(False, validation_alias="DEBUG")
    kin_token: str = Field(..., validation_alias="KIN_TOKEN")

    mongodb_connection_string: str = Field(..., validation_alias="MONGO_DB_CONNECTION_STRING")
    rabbitmq_connection_string: str = Field(..., validation_alias="RABBITMQ_CONNECTION_STRING")

    models_storage_path: str = Field(..., validation_alias="MODELS_STORAGE_PATH")
    allowed_hosts: list[str] = Field(..., validation_alias="ALLOWED_HOSTS")
