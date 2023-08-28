from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    model_storage_path: str = Field(..., env="MODEL_STORAGE_PATH")
    default_stop_words_path: str = Field(..., env="DEFAULT_STOP_WORDS_PATH")
