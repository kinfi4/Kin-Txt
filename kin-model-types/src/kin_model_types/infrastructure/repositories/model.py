import logging
from typing import cast

from sqlalchemy import and_, delete, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from kin_txt_core.database import Database
from kin_txt_core.reports_building.domain.entities import PreprocessingConfig

from kin_model_types.constants import ModelStatuses
from kin_model_types.domain.entities.model import ModelEntity, CreateModelEntity, ModelFilters, UpdateModelEntity
from kin_model_types.exceptions.base import UserModelNotFoundException, ModelAlreadyExistsException
from kin_model_types.types import CategoryMapping
from kin_model_types.infrastructure.models import Model as ORMModel, PreprocessingConfig as ORMPreprocessingConfig


class ModelRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_model(self, model_code: str, username: str) -> ModelEntity:
        with self._db.session() as session:
            session: Session

            orm_model = (
                session.query(ORMModel)
                .filter_by(code=model_code, owner_username=username)
                .options(joinedload(ORMModel.preprocessing_config))
                .first()
            )

        if orm_model is None:
            raise UserModelNotFoundException(f"Model for {username} with code {model_code} not found")

        return self._map_orm_to_model_entity(cast(ORMModel, orm_model))

    def get_user_models(self, username: str, filters: ModelFilters | None = None) -> list[ModelEntity]:
        self._logger.info(f"[ModelRepository] Getting models for user {username} with filters {filters}")

        with self._db.session() as session:
            session: Session

            query = (
                session.query(ORMModel)
                .filter_by(owner_username=username)
                .options(joinedload(ORMModel.preprocessing_config))
            )

            if filters:
                query = query.filter_by(**filters.dict(exclude_none=True))

            models = query.all()

        return [
            self._map_orm_to_model_entity(cast(ORMModel, orm_model))
            for orm_model in models
        ]

    def save_new_model(
        self,
        username: str,
        create_model: CreateModelEntity,
        override_status: ModelStatuses | None = None,
    ) -> ModelEntity:
        self._logger.info(f"[ModelRepository] Saving model for user {username}")

        with self._db.session() as session:
            session: Session

            try:
                model = ORMModel(
                    owner_username=username,
                    model_status=ModelStatuses.CREATED if override_status is None else override_status,
                    **create_model.model_dump(exclude={"preprocessing_config"})
                )

                session.add(model)

                preprocessing_config = ORMPreprocessingConfig(
                    model_code=model.code,
                    **create_model.preprocessing_config.model_dump(),
                )

                session.add(preprocessing_config)

                model_with_preprocessing = (
                    session.query(ORMModel)
                    .filter_by(code=model.code)
                    .options(joinedload(ORMModel.preprocessing_config))
                    .first()
                )
            except IntegrityError:
                self._logger.error(
                    f"[ModelRepository] Model already exists for {username} with code: {create_model.code}"
                )

                raise ModelAlreadyExistsException(f"Model with code {create_model.code} already exists")

        return self._map_orm_to_model_entity(cast(ORMModel, model_with_preprocessing))

    def delete_model(self, model_code: str, username: str) -> None:
        self._logger.info(f"[ModelRepository] Deleting model for user {username}")

        with self._db.session() as session:
            session: Session

            delete_query = (
                delete(ORMModel)
                .where(
                    and_(ORMModel.code == model_code, ORMModel.owner_username == username)
                )
            )

            session.execute(delete_query)

    def update_model(self, model_code: str, username: str, update_model_entity: UpdateModelEntity) -> ModelEntity:
        self._logger.info(f"[ModelRepository] Updating model for user {username}")

        with self._db.session() as session:
            session: Session

            update_preprocessing_query = (
                update(ORMPreprocessingConfig)
                .where(ORMPreprocessingConfig.model_code == model_code)
                .values(update_model_entity.preprocessing_config.model_dump())
            )

            session.execute(update_preprocessing_query)

            update_model_query = (
                update(ORMModel)
                .where(
                    and_(ORMModel.code == model_code, ORMModel.owner_username == username)
                )
                .values(update_model_entity.model_dump(exclude_none=True, exclude={"preprocessing_config", "code"}))
            )
            session.execute(update_model_query)

            orm_model = (
                session.query(ORMModel)
                .filter_by(code=model_code, owner_username=username)
                .options(joinedload(ORMModel.preprocessing_config))
                .first()
            )

        if orm_model is None:
            raise UserModelNotFoundException(f"Model for {username} with code {model_code} not found")

        return self._map_orm_to_model_entity(cast(ORMModel, orm_model))

    def update_model_status(
        self,
        model_code: str,
        username: str,
        status: ModelStatuses,
        validation_message: str | None = None,
    ) -> None:
        with self._db.session() as session:
            session: Session

            model = (
                session.query(ORMModel)
                .filter(
                    and_(
                        ORMModel.code == model_code,
                        ORMModel.owner_username == username,
                    )
                )
                .first()
            )

            model.model_status = status
            if validation_message:
                model.validation_message = validation_message

    def _map_orm_to_model_entity(self, orm_model: ORMModel) -> ModelEntity:
        return ModelEntity(
            code=orm_model.code,
            name=orm_model.name,
            model_type=orm_model.model_type,
            owner_username=orm_model.owner_username,
            category_mapping=CategoryMapping(orm_model.category_mapping),
            model_status=orm_model.model_status,
            validation_message=orm_model.validation_message,
            original_model_file_name=orm_model.original_model_file_name,
            original_tokenizer_file_name=orm_model.original_tokenizer_file_name,
            preprocessing_config=PreprocessingConfig.from_orm(orm_model.preprocessing_config),
        )
