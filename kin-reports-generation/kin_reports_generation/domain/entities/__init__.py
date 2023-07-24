from pydantic import BaseModel

from .generate_report import GenerateReportEntity
from .reports import BaseReport, WordCloudReport, StatisticalReport
from .user import User
from .model import ModelEntity, CreateModelEntity
from .model_validation import ModelValidationEntity, UpdateModelEntity
from .visualization_template import VisualizationTemplate

from kin_reports_generation.domain.services.predicting.predictor.interface import IPredictor


class GenerationTemplateWrapper(BaseModel):
    generate_report_metadata: GenerateReportEntity
    model_metadata: ModelEntity
    visualization_template: VisualizationTemplate
    predictor: IPredictor
