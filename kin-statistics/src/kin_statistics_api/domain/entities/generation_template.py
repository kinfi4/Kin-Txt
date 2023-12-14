from datetime import datetime

from pydantic import BaseModel, Field

from kin_txt_core.datasources.constants import DataSourceTypes
from kin_statistics_api.constants import ReportTypes


class GenerationTemplate(BaseModel):
    id: str | None
    name: str

    channel_list: list[str] = Field(..., alias="channelList")
    from_date: datetime = Field(..., alias="fromDate")
    to_date: datetime = Field(..., alias="toDate")
    report_type: ReportTypes = Field(..., alias="reportType")
    template_id: str = Field(..., alias="templateId")
    model_code: str = Field(..., alias="modelCode")
    report_name: str = Field(..., alias="reportName")
    datasource: DataSourceTypes = Field(DataSourceTypes.TELEGRAM)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
