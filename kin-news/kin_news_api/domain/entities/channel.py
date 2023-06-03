from pydantic import BaseModel, Field, validator, root_validator

from domain.utils import truncate_channel_link_to_username


class ChannelPostEntity(BaseModel):
    link: str

    @validator("link", pre=True, allow_reuse=True)
    def _extract_link(cls, link: str) -> str:
        return truncate_channel_link_to_username(link)



class ChannelGetEntity(BaseModel):
    link: str
    title: str
    description: str
    participants_count: str = Field(..., alias="subscribersNumber")
    profile_photo_url: str | None = Field(..., alias="profilePhotoUrl")

    _extract_link = validator("link", pre=True, allow_reuse=True)(truncate_channel_link_to_username)

    class Config:
        allow_population_by_field_name = True
