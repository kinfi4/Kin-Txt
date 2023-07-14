import os
from datetime import datetime

from pydantic import BaseModel, validator


class LoadPostsConfig(BaseModel):
    start_date: datetime
    end_date: datetime
    channels: list[str]
    output_file_path: str

    @validator("output_file_path")
    def validate_output_file_path(cls, value: str) -> str:
        if not value.endswith(".csv"):
            raise ValueError("Output file path must be csv file")

        return value
