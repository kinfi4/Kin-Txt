from pydantic import BaseModel, Field, root_validator

from kin_reports_generation.constants import VisualizationDiagramTypes, RawContentTypes


class VisualizationTemplate(BaseModel):
    id: str | None = Field(None)
    name: str
    content_types: list[RawContentTypes] | None = Field(None, alias="contentTypes")
    visualization_diagram_types: list[VisualizationDiagramTypes] = Field(..., alias="visualizationDiagramTypes")

    @root_validator
    def validate_content_types(cls, values: dict[str, str | list[str]]) -> dict[str, str | list[str]]:
        content_types_set: set[RawContentTypes] = set()

        for visualization_diagram_type in values.get("visualization_diagram_types"):
            if "__" not in visualization_diagram_type:
                raise ValueError("Invalid visualization_diagram_type")

            content_type, diagram_type = visualization_diagram_type.split("__")

            if content_type not in RawContentTypes.__members__:
                raise ValueError("Invalid content_type")
            if diagram_type not in VisualizationDiagramTypes.__members__:
                raise ValueError("Invalid diagram_type")

            content_types_set.add(content_type)

        values["content_types"] = list(content_types_set) if content_types_set else None

        if not values["content_types"]:
            raise ValueError("At least one content type must be selected")

        return values

    class Config:
        allow_population_by_field_name = True
