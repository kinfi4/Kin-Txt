import logging
from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from kin_txt_core.database import Database

from kin_statistics_api.domain.entities.generation_template import GenerationTemplate as GenerationTemplateEntity
from kin_statistics_api.infrastructure.models import GenerationTemplate as GenerationTemplateORM
from kin_statistics_api.exceptions import GenerationTemplateNotFound


class TemplatesRepository:
    def __init__(self, db: Database) -> None:
        self._db = db
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_template_names(self, username: str) -> list[dict[str, int | str]]:
        with self._db.session() as session:
            session: Session

            user_templates_list = (
                session.query(GenerationTemplateORM.name, GenerationTemplateORM.id)
                .filter(GenerationTemplateORM.owner_username == username)
                .all()
            )

        return [
            {
                "name": template[0],
                "id": template[1],
            }
            for template in user_templates_list
        ]

    def load_user_template(self, username: str, template_id: int) -> GenerationTemplateEntity:
        self._logger.info(f"[TemplatesMongoRepository] Loading {username} template with id: {template_id}")

        with self._db.session() as session:
            session: Session

            generation_template_orm = (
                session.query(GenerationTemplateORM)
                .filter(
                    and_(
                        GenerationTemplateORM.owner_username == username,
                        GenerationTemplateORM.id == template_id,
                    )
                )
                .first()
            )

        if generation_template_orm is None:
            raise GenerationTemplateNotFound(f"Template with id: {template_id} not found.")

        return self._map_orm_to_template_entity(cast(GenerationTemplateORM, generation_template_orm))

    def save_user_template(self, username: str, template: GenerationTemplateEntity) -> None:
        self._logger.info(f"[TemplatesMongoRepository] Saving user template with name: {template.name}")

        template_orm = GenerationTemplateORM(
            owner_username=username,
            **template.model_dump(),
        )

        with self._db.session() as session:
            session: Session

            session.add(template_orm)

    def delete_template(self, username: str, template_id: str) -> None:
        with self._db.session() as session:
            session: Session

            template = (
                session.query(GenerationTemplateORM)
                .filter(
                    and_(
                        GenerationTemplateORM.id == template_id,
                        GenerationTemplateORM.owner_username == username
                    )
                )
                .first()
            )

            if template is None:
                raise GenerationTemplateNotFound(f"Template with id: {template_id} not found.")

            session.delete(template)

    def _map_orm_to_template_entity(self, orm_entity: GenerationTemplateORM) -> GenerationTemplateEntity:
        return GenerationTemplateEntity(
            id=orm_entity.id,
            name=orm_entity.name,
            channel_list=orm_entity.channel_list,
            from_date=orm_entity.from_date,
            to_date=orm_entity.to_date,
            report_type=orm_entity.report_type,
            template_id=orm_entity.template_id,
            model_code=orm_entity.model_code,
            report_name=orm_entity.report_name,
            model_type=orm_entity.model_type,
            datasource_type=orm_entity.datasource_type,
        )
