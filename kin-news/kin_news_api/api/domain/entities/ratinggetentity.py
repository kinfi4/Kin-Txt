from pydantic import BaseModel, Field, validator

from api.domain.utils import truncate_channel_link_to_username
from api.models import PossibleRating


class RatePostEntity(BaseModel):
    channel_link: str = Field(..., alias='channelLink')
    rating: PossibleRating

    _extract_link = validator('channel_link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)

    class Config:
        allow_population_by_field_name = True


class RatingGetEntity(BaseModel):
    channel_link: str = Field(..., alias='channelLink')
    my_rate: PossibleRating = Field(..., alias='myRate')
    total_rates: int = Field(..., alias='totalRates')
    average_rating: float = Field(..., alias='averageRating')

    _extract_link = validator('channel_link', pre=True, allow_reuse=True)(truncate_channel_link_to_username)

    class Config:
        allow_population_by_field_name = True
