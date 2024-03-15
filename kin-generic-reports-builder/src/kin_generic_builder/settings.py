from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(..., validation_alias="DEBUG")

    model_storage_path: str = Field(..., validation_alias="MODEL_STORAGE_PATH")
    allowed_hosts: str = Field(..., validation_alias="ALLOWED_HOSTS")

    model_config = ConfigDict(protected_namespaces=())
