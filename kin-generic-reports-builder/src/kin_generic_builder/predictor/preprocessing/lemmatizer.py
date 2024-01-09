import spacy

from kin_txt_core.reports_building.constants import SupportedLanguages
from kin_txt_core.reports_building.domain.entities import PreprocessingConfig


class Lemmatizer:
    _lang_to_model = {
        SupportedLanguages.RU: "ru_core_news_lg",
        SupportedLanguages.EN: "en_core_web_lg",
        SupportedLanguages.UK: "uk_core_news_trf",
    }

    def __init__(self) -> None:
        self._nlp_models = {}

    def lemmatize_text(self, text: str, settings: PreprocessingConfig) -> str:
        if settings.language == SupportedLanguages.OTHER:
            return text

        if settings.language not in self._nlp_models:
            language_model = self._lang_to_model[settings.language]
            self._nlp_models[settings.language] = spacy.load(language_model)

        nlp = self._nlp_models[settings.language]
        return " ".join([token.lemma_ for token in nlp(text)])
