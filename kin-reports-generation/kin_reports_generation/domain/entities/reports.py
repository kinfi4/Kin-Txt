from typing import Any, Optional, Generic, TypeVar, TypeAlias
from datetime import datetime

from pydantic import BaseModel, Field, validator

from kin_news_core.constants import DEFAULT_DATETIME_FORMAT
from kin_reports_generation.constants import (
    ReportProcessingResult,
    ReportTypes,
    VisualizationDiagrams,
)

TPostsCategories = TypeVar("TPostsCategories", bound=dict[int, str])

DataByCategory: TypeAlias = dict[TPostsCategories, int]
DataByDateChannelCategory: TypeAlias = dict[str, DataByCategory]


class BaseReport(BaseModel, Generic[TPostsCategories]):
    report_id: int = Field(..., alias="reportId")
    name: str = Field(max_length=80)
    report_type: ReportTypes = Field(ReportTypes.STATISTICAL, alias="reportType")
    processing_status: ReportProcessingResult = Field(..., alias="processingStatus")
    generation_date: datetime = Field(..., alias="generationDate")
    posts_categories: TPostsCategories = Field(..., alias="postsCategories")

    report_failed_reason: str | None = Field(None, alias="reportFailedReason")

    @validator("generation_date", pre=True)
    def parse_generation_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, DEFAULT_DATETIME_FORMAT)  # parse a string into datetime

        return value

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.strftime(DEFAULT_DATETIME_FORMAT)}


class StatisticalReport(BaseReport):
    total_messages_count: int | None = Field(None, alias="totalMessagesCount")

    set_of_visualization_diagrams: set[VisualizationDiagrams] | None = Field(None, alias="setOfVisualizationDiagrams")
    data: dict[VisualizationDiagrams, DataByCategory | DataByDateChannelCategory] | None = Field(None, alias="data")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, dict_report: dict[str, Any]) -> "StatisticalReport":
        return cls(
            report_id=dict_report["report_id"],
            report_type=dict_report["report_type"],
            name=dict_report["name"],
            processing_status=dict_report["processing_status"],
            report_failed_reason=dict_report["report_failed_reason"],
            total_messages_count=dict_report["total_messages_count"],
            set_of_visualization_diagrams=dict_report["set_of_visualization_diagrams"],
            data=dict_report["data"],
        )


class WordCloudReport(BaseReport):
    total_words: int | None = Field(None, alias="totalWords")
    total_words_frequency: list[tuple[str, int]] | None = Field(None, alias="totalWordsFrequency")
    data_by_channel: dict[str, list[tuple[str, int]]] | None = Field(None, alias="dataByChannel")

    data_by_category: Optional[
        dict[TPostsCategories, list[tuple[str, int]]]
    ] = Field(None, alias="dataByCategory")

    data_by_channel_by_category: Optional[
        dict[str, dict[TPostsCategories, list[tuple[str, int]]]]
    ] = Field(None, alias="dataByChannelByCategory")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, dict_report: dict[str, Any]) -> "WordCloudReport":
        return cls(
            report_id=dict_report["report_id"],
            report_type=dict_report["report_type"],
            name=dict_report["name"],
            processing_status=dict_report["processing_status"],
            report_failed_reason=dict_report.get("report_failed_reason"),
            total_words=dict_report.get("total_words"),
            data_by_channel_by_category=dict_report.get("data_by_channel_by_category"),
            data_by_category=dict_report.get("data_by_category"),
            data_by_channel=dict_report.get("data_by_channel"),
            total_words_frequency=dict_report.get("total_words_frequency"),
        )
