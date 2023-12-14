from pydantic import Field, BaseSettings


class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    debug: bool = Field(False, env="DEBUG")
    kin_token: str = Field(..., env="KIN_TOKEN")

    mongodb_connection_string: str = Field(..., env="MONGO_DB_CONNECTION_STRING")
    rabbitmq_connection_string: str = Field(..., env="RABBITMQ_CONNECTION_STRING")

    models_storage_path: str = Field(..., env="MODELS_STORAGE_PATH")
