import logging
from typing import Mapping, TypeAlias

from bson import ObjectId
from pymongo import MongoClient

from kin_model_types import Settings
from kin_model_types.constants import ModelStatuses
from kin_model_types.domain.entities import ModelEntity, ModelValidationEntity, ModelFilters
from kin_model_types.exceptions.base import UserModelNotFoundException
from kin_model_types.types import CategoryMapping

ModelDict: TypeAlias = dict[str, str | ModelStatuses, CategoryMapping]


class ModelRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_generation_db = mongo_client["reports_generation_service"]
        self._models_collection = self._reports_generation_db["models"]

        self._logger = logging.getLogger(self.__class__.__name__)

        self._models_collection.create_index("code", unique=True)

    def get_model(self, model_code: str, username: str) -> ModelEntity:
        model_dict = self._models_collection.find_one(
            {"code": model_code, "owner_username": username}
        )

        if model_dict is None:
            raise UserModelNotFoundException(f"Model for {username} with code {model_code} not found")

        return self._map_dict_to_model_entity(model_dict)

    def get_user_models(self, username: str, filters: ModelFilters | None = None) -> list[ModelEntity]:
        self._logger.info(f"[ModelRepository] Getting models for user {username} with filters {filters}")

        filters_dict = {"owner_username": username}

        if filters:
            filters_dict.update(filters.dict(exclude_none=True))

        models_dicts = self._models_collection.find(filters_dict)

        return [
            self._map_dict_to_model_entity(model_dict)
            for model_dict in models_dicts
        ]

    def save_new_model(self, model: ModelValidationEntity) -> ModelEntity:
        self._logger.info(f"[ModelRepository] Saving model for user {model.owner_username}")

        model_dict = model.dict()
        model_dict["model_status"] = ModelStatuses.CREATED
        inserted_id = self._models_collection.insert_one(model_dict).inserted_id

        model_dict = self._models_collection.find_one({"_id": ObjectId(inserted_id)})
        return self._map_dict_to_model_entity(model_dict)

    def delete_model(self, model_code: str, username: str) -> None:
        self.get_model(model_code, username).delete_binaries(Settings().models_storage_path)
        self._models_collection.delete_one({"code": model_code, "owner_username": username})

    def update_model(self, model_code: str, username: str, model_dict: ModelDict) -> ModelEntity:
        self._logger.info(f"[ModelRepository] Updating model for user {username}")

        returned_model = self._models_collection.find_one_and_update(
            {"code": model_code, "owner_username": username},
            {"$set": model_dict},
            return_document=True,
        )

        return self._map_dict_to_model_entity(returned_model)

    def update_model_status(self, model_code: str, username: str, status: ModelStatuses) -> None:
        self._models_collection.find_one_and_update(
            {"code": model_code, "owner_username": username},
            {"$set": {"model_status": status}},
        )

    def _map_dict_to_model_entity(self, model_dict: Mapping[str, str | list[CategoryMapping]]) -> ModelEntity:
        return ModelEntity(
            code=model_dict["code"],
            name=model_dict["name"],
            model_type=model_dict["model_type"],
            owner_username=model_dict["owner_username"],
            category_mapping=model_dict["category_mapping"],
            model_status=model_dict["model_status"],
            validation_message=model_dict.get("validation_message"),
        )
