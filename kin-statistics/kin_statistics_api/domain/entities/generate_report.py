from datetime import date, datetime
from typing import Any, Optional, Union

from django.conf import settings
from pydantic import BaseModel, Field, ValidationError, root_validator, validator

from config.constants import DEFAULT_DATE_FORMAT, ReportTypes


def _cast_string_to_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, DEFAULT_DATE_FORMAT).date()
    except ValueError:
        raise ValueError('Invalid string format for incoming StartDate field!')


class GenerateReportEntity(BaseModel):
    start_date: date = Field(..., alias='startDate')
    end_date: date = Field(..., alias='endDate')
    channel_list: list[str] = Field(..., alias='channels')
    report_type: Optional[ReportTypes] = Field(None, alias='reportType')

    @validator('channel_list', pre=True, allow_reuse=True)
    def validate_channels(cls, channels: list[str]) -> list[str]:
        if len(channels) > settings.MAX_SUBSCRIPTIONS_ALLOWED or not channels:
            raise ValidationError('You passed invalid list of channels to process!')

        return channels

    @validator('start_date', pre=True)
    def validate_and_cast_start_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value

    @validator('end_date', pre=True)
    def validate_and_cast_end_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value

    @root_validator()
    def validate_start_and_end_dates_difference(cls, fields: dict[str, Any]):
        if fields['end_date'] < fields['start_date']:
            raise ValueError('Start date must be earlier than end date.')

        if (fields['end_date'] - fields['start_date']).days > 365:
            raise ValueError('The period of time between start and end dates must be less than 1 year')

        return fields

    class Config:
        allow_population_by_field_name = True
