from typing import Any, Optional
from datetime import datetime

from pydantic import field_validator, field_serializer, ConfigDict, BaseModel, Field
from pydantic_core.core_schema import FieldSerializationInfo

from kin_txt_core.constants import DEFAULT_DATETIME_FORMAT
from kin_txt_core.types.reports import (
    RawContentTypes,
    VisualizationDiagramTypes,
    DataByCategory,
    DataByDateChannelCategory,
)
from kin_statistics_api.constants import (
    ReportProcessingResult,
    ReportTypes,
)


class BaseReport(BaseModel):
    report_id: int = Field(..., alias="reportId")
    name: str = Field(max_length=80)
    report_type: ReportTypes = Field(ReportTypes.STATISTICAL, alias="reportType")
    processing_status: ReportProcessingResult = Field(..., alias="processingStatus")
    generation_date: datetime = Field(..., alias="generationDate")

    report_failed_reason: str | None = Field(None, alias="reportFailedReason")
    report_warnings: list[str] | None = Field(None, alias="reportWarnings")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("generation_date", mode="before")
    def parse_generation_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, DEFAULT_DATETIME_FORMAT)  # parse a string into datetime

        return value

    @field_serializer("generation_date", when_used="json")
    @staticmethod
    def serialize_generation_date(value: datetime, _info: FieldSerializationInfo) -> str:
        return value.strftime(DEFAULT_DATETIME_FORMAT)


class StatisticalReport(BaseReport):
    total_messages_count: int | None = Field(None, alias="totalMessagesCount")
    posts_categories: list[str] | None = Field(None, alias="postsCategories")
    visualization_diagrams_list: list[VisualizationDiagramTypes] | None = Field(None, alias="visualizationDiagramsList")

    data: dict[RawContentTypes, DataByCategory | DataByDateChannelCategory] | None = Field(None, alias="data")

    model_config = ConfigDict(populate_by_name=True)


class WordCloudReport(BaseReport):
    posts_categories: list[str] | None = Field(..., alias="postsCategories")

    total_words: int | None = Field(None, alias="totalWords")
    total_words_frequency: list[tuple[str, int]] | None = Field(None, alias="totalWordsFrequency")
    data_by_channel: dict[str, list[tuple[str, int]]] | None = Field(None, alias="dataByChannel")

    data_by_category: Optional[
        dict[str, list[tuple[str, int]]]
    ] = Field(None, alias="dataByCategory")

    data_by_channel_by_category: Optional[
        dict[str, dict[str, list[tuple[str, int]]]]
    ] = Field(None, alias="dataByChannelByCategory")

    model_config = ConfigDict(populate_by_name=True)


class ReportPutEntity(BaseModel):
    name: str = Field(..., max_length=80)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("name", mode="before")
    def name_must_be_unique(cls, value: str) -> str:
        if len(value) < 1:
            raise ValueError("Name must be at least 1 character long!")

        return value


class ReportIdentificationEntity(BaseReport):
    pass
