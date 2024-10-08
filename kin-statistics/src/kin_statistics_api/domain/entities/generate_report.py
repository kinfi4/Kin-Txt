from datetime import date, datetime

from pydantic import field_validator, model_validator, ConfigDict, BaseModel, Field, ValidationError

from kin_txt_core.constants import DEFAULT_DATE_FORMAT
from kin_txt_core.datasources.constants import DataSourceTypes
from kin_statistics_api.constants import ReportTypes
from kin_statistics_api.settings import Settings
from kin_txt_core.reports_building.constants import ModelTypes, ClassificationScopes


def _cast_string_to_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, DEFAULT_DATE_FORMAT).date()
    except ValueError:
        raise ValueError("Invalid string format for incoming StartDate field!")


class GenerateReportEntity(BaseModel):
    name: str = Field(..., max_length=80)
    model_code: str = Field(..., alias="modelCode")
    template_id: int | None = Field(..., alias="templateId")
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    channel_list: list[str] = Field(..., alias="channels")
    report_type: ReportTypes = Field(..., alias="reportType")
    datasource_type: DataSourceTypes = Field(DataSourceTypes.TELEGRAM, alias="datasourceType")
    model_type: ModelTypes = Field(..., alias="modelType")
    classification_scope: ClassificationScopes = Field(ClassificationScopes.ENTIRE_POST, alias="classificationScope")

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    @field_validator("template_id", mode="before")
    def validate_template_id(cls, template_id: int | None) -> int | None:
        if template_id is None or template_id == "":
            return None

        return template_id

    @field_validator("channel_list", mode="before")
    def validate_channels(cls, channels: list[str]) -> list[str]:
        if not channels:
            raise ValueError("You have to pass at least one channel to gather information from!")

        if len(channels) > Settings().max_channel_per_report_count:
            raise ValueError(f"Maximum channels per report is {Settings().max_channel_per_report_count}")

        return channels

    @field_validator("start_date", "end_date", mode="before")
    def validate_and_cast_start_date(cls, value: str | date):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value

    @model_validator(mode="after")
    def validate_start_and_end_dates_difference(self) -> "GenerateReportEntity":
        if self.end_date < self.start_date:
            raise ValueError("Start date must be earlier than end date.")

        if self.start_date > date.today():
            raise ValueError("Start date must be earlier than today.")

        if (self.end_date - self.start_date).days > 365:
            raise ValueError("The period of time between start and end dates must be less than 1 year")

        if self.report_type == ReportTypes.STATISTICAL and self.template_id is None:
            raise ValueError("Template id must be specified for statistical report type.")

        if self.report_type == ReportTypes.STATISTICAL and self.classification_scope == ClassificationScopes.TOKENS:
            raise ValueError("Statistical report currently does not support token classification scope.")

        return self
