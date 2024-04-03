from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_storage_path: str = Field(..., env="MODEL_STORAGE_PATH")
