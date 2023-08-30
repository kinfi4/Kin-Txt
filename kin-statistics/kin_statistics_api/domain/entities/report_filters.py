from datetime import datetime

from pydantic import BaseModel, Field

from kin_statistics_api.constants import ReportProcessingResult


class ReportFilters(BaseModel):
    page: int = 0
    name: str | None = Field(None, min_length=1, max_length=255)
    date_from: datetime | None = Field(None, alias="dateFrom")
    date_to: datetime | None = Field(None, alias="dateTo")
    processing_status: ReportProcessingResult | None = Field(None, min_length=1, max_length=10, alias="processingStatus")

    class Config:
        allow_population_by_field_name = True
