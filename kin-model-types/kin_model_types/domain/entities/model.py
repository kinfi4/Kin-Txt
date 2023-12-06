import json

from pydantic import BaseModel, Field, validator

from kin_model_types.constants import ModelStatuses
from kin_model_types.types import CategoryMapping
from kin_model_types.constants import ModelTypes


class ModelFilters(BaseModel):
    model_status: ModelStatuses | None = Field(None, alias="modelStatus")


class ModelValidationEntity(BaseModel):
    name: str
    code: str
    owner_username: str = Field(..., alias="ownerUsername")
    model_type: ModelTypes = Field(..., alias="modelType")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")
    original_model_file_name: str | None = Field(None, alias="originalModelFileName")
    original_tokenizer_file_name: str | None = Field(None, alias="originalTokenizerFileName")

    class Config:
        allow_population_by_field_name = True


class ModelEntity(ModelValidationEntity):
    model_status: ModelStatuses = Field(..., alias="modelStatus")
    validation_message: str | None = Field(None, alias="validationMessage")


class CreateModelEntity(BaseModel):
    name: str
    code: str
    model_type: ModelTypes = Field(..., alias="modelType")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping", )
    original_model_file_name: str | None = Field(None, alias="originalModelFileName")
    original_tokenizer_file_name: str | None = Field(None, alias="originalTokenizerFileName")

    class Config:
        allow_population_by_field_name = True

    @validator("category_mapping", pre=True)
    def parse_json(cls, mappings_value: dict | str) -> dict:
        if isinstance(mappings_value, str):
            try:
                return json.loads(mappings_value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")

        return mappings_value


class UpdateModelEntity(CreateModelEntity):
    models_has_changed: bool = Field(False, alias="modelsHasChanged")


class CustomModelRegistrationEntity(BaseModel):
    name: str
    code: str
    owner_username: str = Field(..., alias="ownerUsername")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")
