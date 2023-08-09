from typing import Any

from pydantic import BaseModel, root_validator

from .generate_report import GenerateReportEntity
from .reports import BaseReport, WordCloudReport, StatisticalReport
from .user import User
from .model import ModelEntity, CreateModelEntity, ModelValidationEntity, UpdateModelEntity
from .visualization_template import VisualizationTemplate

from kin_reports_generation.domain.services.predicting.predictor.interface import IPredictor
from kin_reports_generation.constants import ReportTypes


class GenerationTemplateWrapper(BaseModel):
    generate_report_metadata: GenerateReportEntity
    model_metadata: ModelEntity
    predictor: IPredictor
    visualization_template: VisualizationTemplate | None = None

    @root_validator()
    def validate_start_and_end_dates_difference(cls, fields: dict[str, Any]) -> dict[str, Any]:
        if fields["generate_report_metadata"].report_type == ReportTypes.STATISTICAL and fields["generate_report_metadata"].template_id is None:
            raise ValueError("Template id must be specified for statistical report type.")

        return fields

    class Config:
        arbitrary_types_allowed = True
