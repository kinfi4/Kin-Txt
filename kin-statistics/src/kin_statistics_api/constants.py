import datetime
from enum import Enum


PROJECT_TITLE = "Kin-Statistics"
PROJECT_DESCRIPTION = "Kin-Statistics is a service for storing and managing statistical reports."

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
MAX_POST_LEN_IN_WORDS = 20
REPORTS_BUILDER_EXCHANGE = "ReportsBuilder"
REPORTS_STORING_EXCHANGE = "ReportsStoring"

ITEMS_PER_PAGE = 8

API_ROUTE_PATH = "/api/statistics/v1"


class ReportTypes(str, Enum):
    STATISTICAL = "Statistical"
    WORD_CLOUD = "WordCloud"


class ReportProcessingResult(str, Enum):
    POSTPONED = "Postponed"
    READY = "Ready"
    PROCESSING = "Processing"
    NEW = "New"
