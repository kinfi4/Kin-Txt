from enum import Enum
from datetime import datetime

from pydantic import ConfigDict, BaseModel, Field

from kin_statistics_api.constants import ReportProcessingResult, ReportTypes


class OrderByOptions(str, Enum):
    date = "generation_date"


class ReportsFetchSettings(BaseModel):
    page: int = 0
    name: str | None = Field(None, min_length=1, max_length=255)
    report_type: ReportTypes | None = Field(None, alias="reportType")
    date_from: datetime | None = Field(None, alias="dateFrom")
    date_to: datetime | None = Field(None, alias="dateTo")
    processing_status: ReportProcessingResult | None = Field(None, alias="processingStatus")

    descending: bool = True
    order_by: OrderByOptions | None = Field(OrderByOptions.date, alias="orderBy")

    model_config = ConfigDict(populate_by_name=True)
