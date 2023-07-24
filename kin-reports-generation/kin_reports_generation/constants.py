import re
from enum import Enum

PROJECT_TITLE = "Kin-Reports-Generation"
PROJECT_DESCRIPTION = "Kin-Reports-Generation is a service for storing, managing user models, templates and for generating user reports using these models."

REPORTS_GENERATION_EXCHANGE = "ReportsGeneration"
REPORTS_STORING_EXCHANGE = "ReportsStoring"
MAX_POST_LEN_IN_WORDS = 20


class MessageCategories(str, Enum):
    POLITICAL = "Political"
    SHELLING = "Shelling"
    HUMANITARIAN = "Humanitarian"
    ECONOMICAL = "Economical"


class SentimentTypes(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ReportTypes(str, Enum):
    STATISTICAL = "Statistical"
    WORD_CLOUD = "WordCloud"


class ReportProcessingResult(str, Enum):
    POSTPONED = "Postponed"
    READY = "Ready"
    PROCESSING = "Processing"


emoji_regex_compiled = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
    "]+",
    re.UNICODE
)


class RawContentTypes(str, Enum):
    BY_DATE_BY_CATEGORY = "ByDateByCategory"
    BY_CHANNEL_BY_CATEGORY = "ByChannelByCategory"
    BY_CATEGORY = "ByCategory"
    BY_CHANNEL = "ByChannel"
    BY_DATE = "ByDate"
    BY_DAY_HOUR = "ByDayHour"
    BY_DATE_BY_CHANNEL = "ByDateByChannel"


class DiagramTypes(str, Enum):
    PIE = "Pie"
    BAR = "Bar"
    LINE = "Line"
    HISTOGRAM = "Histogram"
    SCATTER = "Scatter"
    HEATMAP = "Heatmap"


def generate_visualization_diagram_types() -> "VisualizationDiagramTypes":
    enum_dict = {}

    for rc in RawContentTypes:
        for dt in DiagramTypes:
            enum_dict[f'{rc}__{dt}'] = f'{rc}__{dt}'

    return type("VisualizationDiagramTypes", (str, Enum), enum_dict)


VisualizationDiagramTypes = generate_visualization_diagram_types()


class ModelTypes(str, Enum):
    SKLEARN = "Sklearn"
    TENSORFLOW_BERT = "Tensorflow Bert"
