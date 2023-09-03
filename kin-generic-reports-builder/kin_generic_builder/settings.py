from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    model_storage_path: str = Field(..., env="MODEL_STORAGE_PATH")
    stop_words_storage_path: str = Field(..., env="STOP_WORDS_STORAGE_PATH")
