from datetime import datetime

from pydantic import BaseModel, Field

from kin_news_core.telegram.entities import TelegramMessageEntity


class MessageGetEntity(BaseModel):
    link: str
    created_at: datetime = Field(..., alias='createdAt')

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_tg_entity(cls, tg_entity: TelegramMessageEntity) -> 'MessageGetEntity':
        return cls(
            link=tg_entity.message_link,
            created_at=tg_entity.created_at,
        )
