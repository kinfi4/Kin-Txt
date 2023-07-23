import logging
from typing import Mapping

from pymongo import MongoClient

from kin_reports_generation.domain.entities import ModelEntity, CreateModelEntity
from kin_reports_generation.exceptions.base import UserModelNotFoundException
from kin_reports_generation.types import CategoryMapping


class ModelRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_generation_db = mongo_client["reports_generation_service"]
        self._models_collection = self._reports_generation_db["models"]

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_model(self, model_id: str, username: str) -> ModelEntity:
        model_dict = self._models_collection.find_one(
            {"_id": model_id, "owner_username": username}
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

    def save_model(self, model: CreateModelEntity) -> None:
        self._logger.info(f"[ModelRepository] Saving model for user {model.owner_username}")

        model_dict = model.dict()
        self._models_collection.insert_one(model_dict)

    def delete_model(self, model_id: str, username: str) -> None:
        self._models_collection.delete_one({"_id": model_id, "owner_username": username})

    def update_model(self, model_id: str, username: str, model: CreateModelEntity) -> None:
        self._models_collection.find_one_and_update(
            {"_id": model_id, "owner_username": username},
            {"$set": model.dict(exclude_none=True)},
        )

    def _map_dict_to_model_entity(self, model_dict: Mapping[str, str | list[CategoryMapping]]) -> ModelEntity:
        return ModelEntity(
            id=model_dict["_id"],
            owner_username=model_dict["owner_username"],
            model_path=model_dict["model_path"],
            tokenizer_path=model_dict["tokenizer_path"],
            category_mapping=model_dict["category_mapping"],
        )
