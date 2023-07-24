from fastapi import UploadFile, Form, File
from pydantic import BaseModel, Field

from kin_reports_generation.constants import ModelStatuses

from kin_reports_generation.types import CategoryMapping
from kin_reports_generation.constants import ModelTypes


class ModelValidationEntity(BaseModel):
    name: str
    owner_username: str = Field(..., alias="ownerUsername")
    model_type: ModelTypes = Field(..., alias="modelType")
    model_path: str = Field(..., alias="modelPath")
    tokenizer_path: str = Field(..., alias="tokenizerPath")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")

    class Config:
        allow_population_by_field_name = True


class ModelEntity(ModelValidationEntity):
    id: str
    model_status: ModelStatuses = Field(..., alias="modelStatus")
    validation_failed_message: str | None = Field(None, alias="validationFailedMessage")


class CreateModelEntity(BaseModel):
    name: str
    model_type: ModelTypes = Field(..., alias="modelType")
    model_data: UploadFile | None = Field(None, alias="modelData")
    tokenizer_data: UploadFile | None = Field(None, alias="tokenizerData")
    category_mapping: CategoryMapping = Field(..., alias="categoryMapping")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        model_type: ModelTypes = Form(..., alias="modelType"),
        category_mapping: CategoryMapping = Form(..., alias="categoryMapping"),
        model_data: UploadFile = File(None, alias="modelData"),
        tokenizer_data: UploadFile = File(None, alias="tokenizerData"),
    ):
        return cls(
            name=name,
            model_type=model_type,
            category_mapping=category_mapping,
            model_data=model_data,
            tokenizer_data=tokenizer_data
        )


class UpdateModelEntity(CreateModelEntity):
    models_has_changed: bool = Field(False, alias="modelsHasChanged")

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        model_type: ModelTypes = Form(..., alias="modelType"),
        category_mapping: CategoryMapping = Form(..., alias="categoryMapping"),
        model_data: UploadFile = File(None, alias="modelData"),
        tokenizer_data: UploadFile = File(None, alias="tokenizerData"),
        models_has_changed: bool = Form(False, alias="modelsHasChanged"),
    ):
        return cls(
            name=name,
            model_type=model_type,
            category_mapping=category_mapping,
            model_data=model_data,
            tokenizer_data=tokenizer_data,
            models_has_changed=models_has_changed
        )
