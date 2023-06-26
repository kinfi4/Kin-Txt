from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, validator

from kin_news_core.constants import DEFAULT_DATETIME_FORMAT
from kin_statistics_api.constants import (
    MessageCategories,
    ReportProcessingResult,
    ReportTypes,
    SentimentTypes,
)


class BaseReport(BaseModel):
    report_id: int = Field(..., alias='reportId')
    name: str = Field(max_length=80)
    report_type: ReportTypes = Field(ReportTypes.STATISTICAL, alias='reportType')
    processing_status: ReportProcessingResult = Field(..., alias='processingStatus')
    generation_date: datetime = Field(..., alias='generationDate')

    report_failed_reason: str | None = Field(None, alias='reportFailedReason')

    @validator("generation_date", pre=True)
    def parse_generation_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.strptime(value, DEFAULT_DATETIME_FORMAT)  # parse a string into datetime

        return value

    def dict(self, with_serialization=False, **kwargs: Any) -> dict[str, Any]:
        model_dict = super().dict(**kwargs)

        if with_serialization:
            model_dict["generationDate"] = self.generation_date.strftime(DEFAULT_DATETIME_FORMAT)

        return model_dict

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.strftime(DEFAULT_DATETIME_FORMAT)}


class StatisticalReport(BaseReport):
    total_messages_count: int | None = Field(None, alias='totalMessagesCount')

    messages_count_by_channel: dict[str, int] | None = Field(None, alias='messagesCountByChannel')
    messages_count_by_date: dict[str, int] | None = Field(None, alias='messagesCountByDate')
    messages_count_by_day_hour: dict[str, int] | None = Field(None, alias='messagesCountByDayHour')
    messages_count_by_category: dict[MessageCategories, int] | None = Field(None, alias='messagesCountByCategory')

    messages_count_by_date_by_category: dict[str, dict[MessageCategories, int]] | None = Field(
        None,
        alias='messagesCountByDateByCategory',
    )

    messages_count_by_channel_by_category: dict[str, dict[MessageCategories, int]] | None = Field(
        None,
        alias='messagesCountByChannelByCategory',
    )

    messages_count_by_sentiment_type: dict[SentimentTypes, int] | None = Field(
        None,
        alias='messagesCountBySentimentType',
    )

    messages_count_by_channel_by_sentiment_type: dict[str, dict[SentimentTypes, int]] | None = Field(
        None,
        alias='messagesCountByChannelBySentimentType',
    )
    messages_count_by_date_by_sentiment_type: dict[str, dict[SentimentTypes, int]] | None = Field(
        None,
        alias='messagesCountByDateBySentimentType',
    )

    @validator('messages_count_by_day_hour', pre=True)
    def _validate_day_hour(cls, messages_dict: dict[str, int]):
        if len(messages_dict) != 24:
            raise ValidationError('Invalid format for messagesCountByDayHour field')

        if any([int(n) not in range(24) for n in messages_dict.keys()]):  # all hours must be between 0 and 23
            raise ValidationError('Invalid format for messagesCountByDayHour field')

        return messages_dict

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, dict_report: dict[str, Any]) -> "StatisticalReport":
        return cls(
            report_id=dict_report['report_id'],
            report_type=dict_report['report_type'],
            name=dict_report['name'],
            processing_status=dict_report['processing_status'],
            generation_date=dict_report['generation_date'],
            report_failed_reason=dict_report['report_failed_reason'],
            total_messages_count=dict_report['total_messages_count'],
            messages_count_by_channel=dict_report['messages_count_by_channel'],
            messages_count_by_date=dict_report['messages_count_by_date'],
            messages_count_by_day_hour=dict_report['messages_count_by_day_hour'],
            messages_count_by_category=dict_report['messages_count_by_category'],
            messages_count_by_date_by_category=dict_report['messages_count_by_date_by_category'],
            messages_count_by_channel_by_category=dict_report['messages_count_by_channel_by_category'],
            messages_count_by_sentiment_type=dict_report['messages_count_by_sentiment_type'],
            messages_count_by_channel_by_sentiment_type=dict_report['messages_count_by_channel_by_sentiment_type'],
            messages_count_by_date_by_sentiment_type=dict_report['messages_count_by_date_by_sentiment_type'],
        )


class WordCloudReport(BaseReport):
    total_words: int | None = Field(None, alias='totalWords')
    total_words_frequency: list[tuple[str, int]] | None = Field(None, alias='totalWordsFrequency')
    data_by_channel: dict[str, list[tuple[str, int]]] | None = Field(None, alias='dataByChannel')

    data_by_category: dict[SentimentTypes | MessageCategories, list[tuple[str, int]]] | None = Field(None, alias='dataByCategory')

    data_by_channel_by_category: dict[str, dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]] | None = Field(None, alias='dataByChannelByCategory')

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, dict_report: dict[str, Any]) -> "WordCloudReport":
        return cls(
            report_id=dict_report['report_id'],
            report_type=dict_report['report_type'],
            name=dict_report['name'],
            processing_status=dict_report['processing_status'],
            generation_date=dict_report['generation_date'],
            report_failed_reason=dict_report.get('report_failed_reason'),
            total_words=dict_report.get('total_words'),
            data_by_channel_by_category=dict_report.get('data_by_channel_by_category'),
            data_by_category=dict_report.get('data_by_category'),
            data_by_channel=dict_report.get('data_by_channel'),
            total_words_frequency=dict_report.get('total_words_frequency'),
        )


class ReportPutEntity(BaseModel):
    name: str = Field(max_length=80)

    class Config:
        allow_population_by_field_name = True


class ReportIdentificationEntity(BaseReport):
    pass
