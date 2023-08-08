import logging
from typing import Mapping
from datetime import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

from kin_statistics_api.domain.entities.generation_template import GenerationTemplate
from kin_statistics_api.exceptions import GenerationTemplateNotFound


class TemplatesRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._templates_db = mongo_client["statistics_service"]
        self._templates_collection = self._templates_db["templates"]

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_template_names(self, username: str) -> list[dict[str, str]]:
        user_templates_list = self._templates_collection.find({"owner_username": username}, {"name": 1, "_id": 1})

        return [
            {
                "name": template["name"],
                "id": str(template["_id"]),
            }
            for template in user_templates_list
        ]

    def load_user_template(self, username: str, template_id: str) -> GenerationTemplate:
        self._logger.info(f"[TemplatesMongoRepository] Loading {username} template with id: {template_id}")

        template_dict = self._templates_collection.find_one(
            {"owner_username": username, "_id": self._get_object_id_from_str(template_id)}
        )

        if template_dict is None:
            raise GenerationTemplateNotFound(f"Template with id: {template_id} not found.")

        return self._map_dict_to_template_entity(template_dict)

    def save_user_template(self, username: str, template: GenerationTemplate) -> None:
        self._logger.info(f"[TemplatesMongoRepository] Saving user template with name: {template.name}")

        template_dict = template.dict()
        template_dict["owner_username"] = username

        self._templates_collection.insert_one(template_dict)

    def delete_template(self, username: str, template_id: str) -> None:
        self._templates_collection.delete_one({"owner_username": username, "_id": self._get_object_id_from_str(template_id)})

    def _map_dict_to_template_entity(self, template_dict: Mapping[str, str | list[str] | datetime]) -> GenerationTemplate:
        return GenerationTemplate(
            id=str(template_dict["_id"]),
            name=template_dict["name"],
            channel_list=template_dict["channel_list"],
            from_date=template_dict["from_date"],
            to_date=template_dict["to_date"],
            report_type=template_dict["report_type"],
            template_id=template_dict["template_id"],
            model_id=template_dict["model_id"],
        )

    def _get_object_id_from_str(self, object_id_str: str) -> ObjectId:
        try:
            return ObjectId(object_id_str)
        except InvalidId:
            raise GenerationTemplateNotFound(f"Template with id {object_id_str} not found")
