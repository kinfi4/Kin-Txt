import logging
from typing import TypeAlias, Mapping

from bson import ObjectId
from pymongo import MongoClient

from kin_reports_generation.domain.entities import VisualizationTemplate
from kin_reports_generation.exceptions import UserTemplateNotFoundException

TemplateDict: TypeAlias = Mapping[str, ObjectId | str | list[str]]


class VisualizationTemplateRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_generation_db = mongo_client["reports_generation_service"]
        self._templates_collection = self._reports_generation_db["templates"]

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_template(self, template_id: str, username: str) -> VisualizationTemplate:
        template_dict = self._templates_collection.find_one(
            {"_id": ObjectId(template_id), "owner_username": username}
        )

        if template_dict is None:
            raise UserTemplateNotFoundException(f"Template for {username} with id {template_id} not found")

        return self._map_dict_to_template_entity(template_dict)

    def get_user_templates(self, username: str) -> list[VisualizationTemplate]:
        templates_dicts = self._templates_collection.find({"owner_username": username})
        return [
            self._map_dict_to_template_entity(template_dict)
            for template_dict in templates_dicts
        ]

    def save_template(self, username: str, template: VisualizationTemplate) -> None:
        self._logger.info(f"[VisualizationTemplateRepository] Saving template for user {username}")

        template_dict = template.dict(exclude_none=True)
        template_dict["owner_username"] = username

        self._templates_collection.insert_one(template_dict)

    def delete_template(self, template_id: str, username: str) -> None:
        self._templates_collection.delete_one({"_id": ObjectId(template_id), "owner_username": username})

    def update_template(self, template_id: str, username: str, template: VisualizationTemplate) -> None:
        if not self._templates_collection.find_one({"_id": ObjectId(template_id), "owner_username": username}):
            raise UserTemplateNotFoundException(f"Template for {username} with id {template_id} not found")

        self._templates_collection.find_one_and_update(
            {"_id": ObjectId(template_id), "owner_username": username},
            {"$set": {
                "name": template.name,
                "content_types": template.content_types,
                "visualization_diagram_types": template.visualization_diagram_types,
            }},
        )

    def _map_dict_to_template_entity(self, template_dict: TemplateDict) -> VisualizationTemplate:
        return VisualizationTemplate(
            id=str(template_dict["_id"]),
            name=template_dict["name"],
            content_types=template_dict["content_types"],
            visualization_diagram_types=template_dict["visualization_diagram_types"],
        )
