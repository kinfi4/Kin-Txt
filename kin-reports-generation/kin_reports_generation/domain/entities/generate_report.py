from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, validator, Field

from kin_reports_generation.constants import ReportTypes, VisualizationDiagrams
from kin_news_core.constants import DEFAULT_DATE_FORMAT
from kin_reports_generation.domain.entities.reports import TPostsCategories


def _cast_string_to_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, DEFAULT_DATE_FORMAT).date()
    except ValueError:
        raise ValueError('Invalid string format for incoming StartDate field!')


class GenerateReportEntity(BaseModel):
    report_id: int
    start_date: date
    end_date: date
    channel_list: list[str]
    report_type: Optional[ReportTypes] = None
    posts_categories: TPostsCategories = Field(..., alias="postsCategories")
    set_of_visualization_diagrams: set[VisualizationDiagrams] | None = Field(None, alias="setOfVisualizationDiagrams")

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

    class Config:
        allow_population_by_field_name = True
