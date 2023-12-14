from kin_news_classification.predictor.predictor import NewsTypePredictor

from kin_txt_core.reports_building.constants import ModelTypes
from kin_txt_core.reports_building.domain.entities import ModelEntity, CustomModelRegistrationEntity
from kin_txt_core.reports_building.domain.services.predicting import IPredictorFactory, IPredictor

__all__ = ["KinBertNewsClassificator"]


class KinBertNewsClassificator(IPredictorFactory):
    model_type: CustomModelRegistrationEntity = CustomModelRegistrationEntity(
        code="kin_bert_news_classificator",
        name="Kin BERT News Classificator",
        owner_username="kinfi4",
        category_mapping={
            "0": "Political",
            "1": "Shelling",
            "2": "Economical",
            "3": "Other",
        },
    )

    def create_predictor(self, model_entity: ModelEntity) -> IPredictor:
        return NewsTypePredictor()

    def is_handling(self, model_type: ModelTypes, model_code: str) -> bool:
        return model_type == ModelTypes.BUILTIN and model_code == self.model_type.code
