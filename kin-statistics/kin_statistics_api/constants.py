import re
from enum import Enum


class MessageCategories(str, Enum):
    POLITICAL = 'Political'
    SHELLING = 'Shelling'
    HUMANITARIAN = 'Humanitarian'
    ECONOMICAL = 'Economical'


DEFAULT_DATE_FORMAT = '%d/%m/%Y'


class ReportProcessingResult(str, Enum):
    POSTPONED = 'Postponed'
    READY = 'Ready'
    PROCESSING = 'Processing'


MAX_POST_LEN_IN_WORDS = 20


class SentimentTypes(str, Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'


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


class ReportTypes(str, Enum):
    STATISTICAL = 'Statistical'
    WORD_CLOUD = 'WordCloud'
