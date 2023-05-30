from pydantic import BaseSettings, Field

from kin_news_core.settings import PostgresSettings, TelegramSettings


class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    debug: bool = Field(False, env="DEBUG")
    token_life_minutes: int = Field(..., env="TOKEN_LIFE_MINUTES")
    max_user_subscriptions_count: int = Field(12, env="MAX_USER_SUBSCRIPTIONS_COUNT")
    statistics_service_url: str = Field(..., env="STATISTICS_SERVICE_URL")
    media_root: str = Field(..., env="MEDIA_ROOT")

    allowed_hosts: list[str] = Field(..., env="ALLOWED_HOSTS")
    kin_token: str = Field(..., env="KIN_TOKEN")

    database: PostgresSettings = PostgresSettings()
    telegram: TelegramSettings = TelegramSettings()
