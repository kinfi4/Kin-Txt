import logging
from typing import Mapping, TypeAlias

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

from kin_reports_generation.constants import ModelStatuses
from kin_reports_generation.domain.entities import ModelEntity, ModelValidationEntity
from kin_reports_generation.exceptions.base import UserModelNotFoundException
from kin_reports_generation.types import CategoryMapping

ModelDict: TypeAlias = dict[str, str | ModelStatuses, CategoryMapping]


class ModelRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_generation_db = mongo_client["reports_generation_service"]
        self._models_collection = self._reports_generation_db["models"]

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_model(self, model_id: str, username: str) -> ModelEntity:
        model_dict = self._models_collection.find_one(
            {"_id": self._get_object_id_from_str(model_id), "owner_username": username}
        )

        if model_dict is None:
            raise UserModelNotFoundException(f"Model for {username} with id {model_id} not found")

        return self._map_dict_to_model_entity(model_dict)

    def get_user_models(self, username: str) -> list[ModelEntity]:
        models_dicts = self._models_collection.find({"owner_username": username})
        return [
            self._map_dict_to_model_entity(model_dict)
            for model_dict in models_dicts
        ]

    def save_new_model(self, model: ModelValidationEntity) -> ModelEntity:
        self._logger.info(f"[ModelRepository] Saving model for user {model.owner_username}")

        model_dict = model.dict()
        model_dict["model_status"] = ModelStatuses.CREATED
        inserted_id = self._models_collection.insert_one(model_dict).inserted_id

        return self.get_model(str(inserted_id), model.owner_username)

    def delete_model(self, model_id: str, username: str) -> None:
        self._models_collection.delete_one({"_id": self._get_object_id_from_str(model_id), "owner_username": username})

    def update_model(self, model_id: str, username: str, model_dict: ModelDict) -> ModelEntity:
        returned_model = self._models_collection.find_one_and_update(
            {"_id": self._get_object_id_from_str(model_id), "owner_username": username},
            {"$set": model_dict},
            return_document=True,
        )

        return self._map_dict_to_model_entity(returned_model)

    def update_model_status(self, model_id: str, username: str, status: ModelStatuses) -> None:
        self._models_collection.find_one_and_update(
            {"_id": self._get_object_id_from_str(model_id), "owner_username": username},
            {"$set": {"model_status": status}},
        )

    def _get_object_id_from_str(self, model_id: str) -> ObjectId:
        try:
            return ObjectId(model_id)
        except InvalidId:
            raise UserModelNotFoundException(f"Model with id {model_id} not found")

    def _map_dict_to_model_entity(self, model_dict: Mapping[str, ObjectId | str | list[CategoryMapping]]) -> ModelEntity:
        return ModelEntity(
            id=str(model_dict["_id"]),
            name=model_dict["name"],
            model_type=model_dict["model_type"],
            owner_username=model_dict["owner_username"],
            model_path=model_dict["model_path"],
            tokenizer_path=model_dict["tokenizer_path"],
            category_mapping=model_dict["category_mapping"],
            model_status=model_dict["model_status"],
            validation_message=model_dict.get("validation_message"),
        )
