import torch
import spacy
from transformers import BertTokenizer, BertForSequenceClassification

from kin_txt_core.datasources.common.entities import ClassificationEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictor
from kin_txt_core.reports_building.constants import ReportTypes


class EnglishSentimentPredictor(IPredictor):
    MODEL_NAME = "textattack/bert-base-uncased-SST-2"
    _MAPPINGS: dict[int, str] = {
        0: "Negative",
        1: "Positive",
    }

    def __init__(self, report_type: ReportTypes):
        super().__init__()

        self.report_type = report_type

        self.model = BertForSequenceClassification.from_pretrained(self.MODEL_NAME)
        self.tokenizer = BertTokenizer.from_pretrained(self.MODEL_NAME)

        self.en_nlp = spacy.load("en_core_web_lg")

    def predict(self, entity: ClassificationEntity) -> str:
        inputs = self.tokenizer(entity.text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = self.model(**inputs)
        prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sent_idx = prediction[0].argmax()

        return self._MAPPINGS[int(sent_idx)]

    def preprocess_text(self, text: str) -> str:
        if self.report_type == ReportTypes.WORD_CLOUD:
            return self._make_wc_preprocessing(text)

        return text

    def _make_wc_preprocessing(self, text: str) -> str:
        doc = self.en_nlp(text)
        filtered_tokens = [token for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return " ".join([token.lemma_ for token in filtered_tokens])
