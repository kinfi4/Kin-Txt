from pydantic import BaseModel, Field

from kin_reports_generation.constants import ModelTypes
from kin_reports_generation.types import CategoryMapping


class CreateModelEntity(BaseModel):
    name: str
    model_type: ModelTypes = Field(..., alias="modelType")
    owner_username: str = Field(..., alias="ownerUsername")
    model_path: str = Field(..., alias="modelPath")
    tokenizer_path: str = Field(..., alias="tokenizerPath")
    category_list: list[CategoryMapping] = Field(..., alias="categoryList")

    class Config:
        allow_population_by_field_name = True


class ModelEntity(CreateModelEntity):
    id: str
