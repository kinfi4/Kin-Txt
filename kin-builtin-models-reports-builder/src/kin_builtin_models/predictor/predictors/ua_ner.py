import spacy

from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.constants import ReportTypes
from kin_txt_core.reports_building.domain.services.predicting import IPredictor


class UaNerPredictor(IPredictor):
    model_code: str = "ua-ner"
    mapping: dict[str, str] = {
        "LOC": "Location",
        "ORG": "Organization",
        "PER": "Person",
    }

    def __init__(self, report_type: ReportTypes) -> None:
        super().__init__()

        self.report_type = report_type
        self.ua_nlp = spacy.load("uk_core_news_lg")

    def predict_post(self, entity: ClassificationEntity) -> str:
        raise NotImplementedError("Ner doesn't support post prediction")

    def preprocess_text(self, text: str) -> str:
        ...  # doesn't need this method, cause model it not used for post prediction

    def predict_post_tokens(self, entity: ClassificationEntity) -> dict[str, list[str]]:
        document = self.ua_nlp(entity.text)

        words_to_category_mapping = {
            category_name: [] for category_name in self.mapping.values()
        }

        for entity in document.ents:
            if entity.label_ in self.mapping:
                category_name = self.mapping[entity.label_]
                words_to_category_mapping[category_name].append(entity.lemma_)

        return words_to_category_mapping
