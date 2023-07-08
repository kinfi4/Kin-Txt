from datetime import datetime

from pydantic import BaseModel, Field

from kin_statistics_api.constants import ReportTypes


class GenerationTemplate(BaseModel):
    id: str
    name: str
    owner_username: str = Field(..., alias="ownerUsername")

    channel_list: list[str] = Field(..., alias="channelList")
    from_date: datetime = Field(..., alias="fromDate")
    to_date: datetime = Field(..., alias="toDate")
    report_type: ReportTypes = Field(..., alias="reportType")
