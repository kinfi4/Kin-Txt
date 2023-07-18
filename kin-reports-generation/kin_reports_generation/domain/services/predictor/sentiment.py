import os
from collections import namedtuple

from nltk.tokenize import word_tokenize

from kin_reports_generation.domain.services.predictor import IPredictor, ITextPreprocessor
from kin_reports_generation.constants import SentimentTypes

Word = namedtuple('Word', 'form label value')


class CsvFileIndex:
    def __init__(self, filepath: str, delimiter: str = ',', skip_header: bool = True):
        with open(filepath) as csv_file:
            self._lines = csv_file.readlines()[1:] if skip_header else csv_file.readlines()

        self.words = [
            Word(
                form=line.split(delimiter)[0],
                label=line.split(delimiter)[1],
                value=float(line.split(delimiter)[2]),
            )
            for line in self._lines
        ]

    def find_word_binary(self, word: str) -> Word | None:
        word_idx = self._binary_search(0, len(self.words) - 1, word)

        if word_idx is not None:
            return self.words[word_idx]

    def _binary_search(self, left_idx: int, right_idx: int, word: str) -> int | None:
        if right_idx >= left_idx:
            average_idx = int(left_idx + (right_idx - left_idx) / 2)

            if self.words[average_idx].form == word:
                return average_idx
            elif self.words[average_idx].form < word:
                return self._binary_search(average_idx + 1, right_idx, word)
            else:
                return self._binary_search(left_idx, average_idx - 1, word)


class SentimentPredictor(IPredictor):
    _positive_level_threshold = 1
    _negative_level_threshold = -0.1

    def __init__(
        self,
        sentiment_dictionary_filepath: str,
        text_preprocessor: ITextPreprocessor,
    ) -> None:
        if not os.path.exists(sentiment_dictionary_filepath):
            raise AttributeError(f'Sentiment dictionary: {sentiment_dictionary_filepath} does not exist')

        self._word_indexator = CsvFileIndex(sentiment_dictionary_filepath, delimiter=',')
        self._text_preprocessor = text_preprocessor

    def get_category(self, text: str) -> SentimentTypes:
        text = self._text_preprocessor.preprocess_and_lemmatize(text)

        tokens = word_tokenize(text, language='russian')

        tokens_sentiment_values = []
        for token in tokens:
            tokens_sentiment_values.append(self._find_word_sentiment_value(token))

        text_sentiment_value = sum(tokens_sentiment_values)

        if text_sentiment_value > self._positive_level_threshold:
            return SentimentTypes.POSITIVE
        elif text_sentiment_value < self._negative_level_threshold:
            return SentimentTypes.NEGATIVE
        else:
            return SentimentTypes.NEUTRAL

    def _find_word_sentiment_value(self, word: str) -> float:
        word_obj = self._word_indexator.find_word_binary(word)

        return word_obj.value if word_obj is not None else 0
