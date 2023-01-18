from typing import Optional

from pydantic import BaseModel, Field, validator

from api.domain.utils import truncate_channel_link_to_username


class ChannelPostEntity(BaseModel):
    link: str

    _extract_link = validator('link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)


class ChannelGetEntity(BaseModel):
    link: str
    title: str
    description: str
    participants_count: str = Field(..., alias='subscribersNumber')
    profile_photo_url: Optional[str] = Field(..., alias='profilePhotoUrl')

    _extract_link = validator('link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)

    class Config:
        allow_population_by_field_name = True
