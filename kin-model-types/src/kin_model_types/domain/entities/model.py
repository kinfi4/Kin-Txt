import json

from pydantic import field_validator, ConfigDict, BaseModel, Field

from kin_model_types.constants import ModelStatuses
from kin_model_types.types import CategoryMapping
from kin_txt_core.reports_building.constants import ModelTypes
from kin_txt_core.reports_building.domain.entities.preprocessing import PreprocessingConfig


class ModelFilters(BaseModel):
    model_status: ModelStatuses | None = Field(None, alias="modelStatus")

    model_config = ConfigDict(protected_namespaces=())


class ModelValidationEntity(BaseModel):
    name: str
    code: str
    owner_username: str = Field(..., alias="ownerUsername")
    model_type: ModelTypes = Field(..., alias="modelType")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")  # type: ignore
    original_model_file_name: str | None = Field(None, alias="originalModelFileName")
    original_tokenizer_file_name: str | None = Field(None, alias="originalTokenizerFileName")
    preprocessing_config: PreprocessingConfig = Field(..., alias="preprocessingConfig")

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())


class ModelEntity(ModelValidationEntity):
    model_status: ModelStatuses = Field(..., alias="modelStatus")
    validation_message: str | None = Field(None, alias="validationMessage")

    model_config = ConfigDict(protected_namespaces=())


class CreateModelEntity(BaseModel):
    name: str
    code: str
    model_type: ModelTypes = Field(..., alias="modelType")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")  # type: ignore
    original_model_file_name: str | None = Field(None, alias="originalModelFileName")
    original_tokenizer_file_name: str | None = Field(None, alias="originalTokenizerFileName")
    preprocessing_config: PreprocessingConfig = Field(..., alias="preprocessingConfig")

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    @field_validator("category_mapping", mode="before")
    @classmethod
    def parse_json(cls, mappings_value: dict | str) -> dict:
        if isinstance(mappings_value, str):
            try:
                return json.loads(mappings_value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")

        return mappings_value


class UpdateModelEntity(CreateModelEntity):
    pass


class CustomModelRegistrationEntity(BaseModel):
    name: str
    code: str
    owner_username: str
    category_mapping: CategoryMapping  # type: ignore
    preprocessing_config: PreprocessingConfig
    validation_needed: bool = False
