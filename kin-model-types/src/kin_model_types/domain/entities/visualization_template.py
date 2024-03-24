from pydantic import ConfigDict, BaseModel, Field, model_validator

from kin_txt_core.types.reports import VisualizationDiagramTypes, RawContentTypes


class VisualizationTemplate(BaseModel):
    id: int | None = Field(None)
    name: str
    content_types: list[RawContentTypes] | None = Field(None, alias="contentTypes")
    visualization_diagram_types: list[VisualizationDiagramTypes] = Field(..., alias="visualizationDiagramTypes")

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def validate_content_types(self) -> "VisualizationTemplate":
        content_types_set: set[RawContentTypes] = set()

        for visualization_diagram_type in self.visualization_diagram_types:
            if "__" not in visualization_diagram_type:
                raise ValueError("Invalid visualization_diagram_type")

            content_type, diagram_type = visualization_diagram_type.split("__")

            if "+" in content_type:
                content_types_set.add(content_type.split("+")[0])
                content_types_set.add(content_type.split("+")[1])
            else:
                content_types_set.add(content_type)

        self.content_types = list(content_types_set)

        if not self.content_types:
            raise ValueError("At least one content type must be selected")

        return self
