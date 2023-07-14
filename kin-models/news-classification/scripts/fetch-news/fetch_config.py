from datetime import datetime

from pydantic import BaseModel, validator, Field


class LoadPostsConfig(BaseModel):
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime = Field(default_factory=datetime.now)
    channels: list[str] = Field(default_factory=list)
    output_file_path: str

    @validator("output_file_path")
    def validate_output_file_path(cls, value: str) -> str:
        if not value.endswith(".csv"):
            raise ValueError("Output file path must be csv file")

        return value
