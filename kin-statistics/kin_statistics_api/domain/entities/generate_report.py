from datetime import date, datetime
from typing import Any, Union

from pydantic import BaseModel, Field, ValidationError, root_validator, validator

from kin_news_core.constants import DEFAULT_DATE_FORMAT
from kin_statistics_api.constants import ReportTypes
from kin_statistics_api.settings import Settings


def _cast_string_to_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, DEFAULT_DATE_FORMAT).date()
    except ValueError:
        raise ValueError("Invalid string format for incoming StartDate field!")


class GenerateReportEntity(BaseModel):
    name: str = Field(..., max_length=80)
    model_id: str = Field(..., alias="modelId")
    template_id: str | None = Field(..., alias="templateId")
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    channel_list: list[str] = Field(..., alias="channels")
    report_type: ReportTypes = Field(..., alias="reportType")

    @validator("channel_list", pre=True, allow_reuse=True)
    def validate_channels(cls, channels: list[str]) -> list[str]:
        if len(channels) > Settings().max_channel_per_report_count or not channels:
            raise ValidationError("You passed invalid list of channels to process!")

        return channels

    @validator("start_date", pre=True)
    def validate_and_cast_start_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value

    @validator("end_date", pre=True)
    def validate_and_cast_end_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value

    @root_validator()
    def validate_start_and_end_dates_difference(cls, fields: dict[str, Any]):
        if fields["end_date"] < fields["start_date"]:
            raise ValueError("Start date must be earlier than end date.")

        if (fields["end_date"] - fields["start_date"]).days > 365:
            raise ValueError("The period of time between start and end dates must be less than 1 year")

        if fields["report_type"] == ReportTypes.STATISTICAL and fields.get("template_id") is None:
            raise ValueError("Template id must be specified for statistical report type.")

        return fields

    class Config:
        allow_population_by_field_name = True
