from fastapi import UploadFile, Form, File
from pydantic import BaseModel, Field

from kin_reports_generation.types import CategoryMapping
from kin_reports_generation.constants import ModelTypes


class ModelValidationEntity(BaseModel):
    name: str
    model_type: ModelTypes = Field(..., alias="modelType")
    model_data: UploadFile | None = Field(None, alias="modelData")
    tokenizer_data: UploadFile | None = Field(None, alias="tokenizerData")
    category_list: list[CategoryMapping] = Field(..., alias="categoryList")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        model_type: ModelTypes = Form(..., alias="modelType"),
        category_list: list[CategoryMapping] = Form(..., alias="categoryList"),
        model_data: UploadFile = File(None, alias="modelData"),
        tokenizer_data: UploadFile = File(None, alias="tokenizerData"),
    ):
        return cls(
            name=name,
            model_type=model_type,
            category_list=category_list,
            model_data=model_data,
            tokenizer_data=tokenizer_data
        )


class UpdateModelEntity(ModelValidationEntity):
    models_has_changed: bool = Field(False, alias="modelsHasChanged")

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        model_type: ModelTypes = Form(..., alias="modelType"),
        category_list: list[CategoryMapping] = Form(..., alias="categoryList"),
        model_data: UploadFile = File(None, alias="modelData"),
        tokenizer_data: UploadFile = File(None, alias="tokenizerData"),
        models_has_changed: bool = Form(False, alias="modelsHasChanged"),
    ):
        return cls(
            name=name,
            model_type=model_type,
            category_list=category_list,
            model_data=model_data,
            tokenizer_data=tokenizer_data,
            models_has_changed=models_has_changed
        )
