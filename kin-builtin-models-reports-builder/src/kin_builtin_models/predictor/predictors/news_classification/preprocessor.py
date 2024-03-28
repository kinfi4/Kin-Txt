from kin_txt_core.reports_building.domain.services.predicting.preprocessing import ITextPreprocessor


class NewsClassificationPreprocessor(ITextPreprocessor):
    def preprocess_text(self, text: str) -> str:
        return text
