from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    debug: bool = Field(..., env="DEBUG")

    model_storage_path: str = Field(..., env="MODEL_STORAGE_PATH")
    stop_words_storage_path: str = Field(..., env="STOP_WORDS_STORAGE_PATH")
    allowed_hosts: list[str] = Field(..., env="ALLOWED_HOSTS")
