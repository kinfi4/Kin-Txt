import re

import spacy
from spacy.tokens import Token

from kin_txt_core.reports_building.domain.services.predicting.preprocessing import ITextPreprocessor


class NewsClassificationPreprocessor(ITextPreprocessor):
    preprocessing_sub_regexes: list[re.Pattern] = [
        re.compile(r"\*\*|__|~~"),
        re.compile(r'""'),
        re.compile(r'["“”«»„"]\s*["“”«»„"]'),
        re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"),
        re.compile(r"\n|\r|\t"),
        re.compile(r"\[|\]"),
        re.compile(r"\(\s*\)"),
        # re.compile(r"\s+"),
        re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
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
            re.UNICODE,
        ),
    ]

    def __init__(self) -> None:
        self._ru_nlp = spacy.load("ru_core_news_md")
        self._ua_nlp = spacy.load("uk_core_news_md")

    def preprocess_text(self, text: str, lemmatize: bool = False) -> str:
        if lemmatize:
            return self._return_lemmas_only(text)

        return self._make_prediction_preprocessing(text)

    def _make_prediction_preprocessing(self, text: str) -> str:
        for regex in self.preprocessing_sub_regexes:
            text = regex.sub("", text)

        return text.lower().strip()

    def _return_lemmas_only(self, text: str) -> str:
        russian_tokens_list = [token for token in self._ru_nlp(text) if token.is_alpha]
        ukrainian_tokens_list = [token for token in self._ua_nlp(text) if token.is_alpha]

        return self._decide_which_lemmas_to_return(russian_tokens_list, ukrainian_tokens_list)

    def _decide_which_lemmas_to_return(
        self,
        russian_lemmas_list: list[Token],
        ukrainian_lemmas_list: list[Token],
    ) -> str:
        ru_ratio = self._calculate_unchanged_ratio(russian_lemmas_list)
        ua_ratio = self._calculate_unchanged_ratio(ukrainian_lemmas_list)

        # that means that russian lemmatizer didn't recognize a lot of words
        if ru_ratio > ua_ratio:
            return self._get_lemmas_string(ukrainian_lemmas_list)

        return self._get_lemmas_string(russian_lemmas_list)

    @staticmethod
    def _calculate_unchanged_ratio(tokens_list: list[Token]) -> int:
        unchanged = sum(1 for token in tokens_list if token.lemma_ == token.text.lower())

        return unchanged / len(tokens_list) if tokens_list else 0

    @staticmethod
    def _get_lemmas_string(token_list: list[Token]) -> str:
        return " ".join([token.lemma_ for token in token_list if not token.is_stop])
