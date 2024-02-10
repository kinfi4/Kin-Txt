from datetime import datetime

from pydantic import field_validator, field_serializer, ConfigDict, BaseModel, Field

from kin_txt_core.datasources.constants import DataSourceTypes
from kin_statistics_api.constants import ReportTypes
from kin_txt_core.reports_building.constants import ModelTypes


class GenerationTemplate(BaseModel):
    id: str | None = None
    name: str

    channel_list: list[str] = Field(..., alias="channelList")
    from_date: datetime = Field(..., alias="fromDate")
    to_date: datetime = Field(..., alias="toDate")
    report_type: ReportTypes = Field(..., alias="reportType")
    template_id: str = Field(..., alias="templateId")
    model_code: str = Field(..., alias="modelCode")
    report_name: str = Field(..., alias="reportName")
    datasource_type: DataSourceTypes = Field(DataSourceTypes.TELEGRAM, alias="datasourceType")
    model_type: ModelTypes = Field(..., alias="modelType")

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    @field_serializer("from_date", "to_date", when_used="json")
    @staticmethod
    def serialize_date(value: datetime, _info) -> str:
        return value.isoformat()

    @field_validator("from_date", "to_date", mode="before")
    def parse_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, "%m/%d/%Y")
