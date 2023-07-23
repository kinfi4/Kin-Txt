from typing import TypeAlias

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer


CategoryMapping: TypeAlias = dict[int, str]

# Models
SupportedVectorizers: TypeAlias = TfidfVectorizer | CountVectorizer | HashingVectorizer
