import logging
from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from kin_txt_core.database import Database

from kin_model_types.infrastructure.models import VisualizationTemplate as ORMVisualizationTemplate
from kin_model_types.domain.entities import VisualizationTemplate as VisualizationTemplateEntity
from kin_model_types.exceptions import UserTemplateNotFoundException


class VisualizationTemplateRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_template(self, template_id: int, username: str) -> VisualizationTemplateEntity:
        with self._db.session() as session:
            session: Session

            template = (
                session.query(ORMVisualizationTemplate)
                .filter(
                    and_(
                        ORMVisualizationTemplate.owner_username == username,
                        ORMVisualizationTemplate.id == template_id,
                    )
                )
                .first()
            )

        if template is None:
            raise UserTemplateNotFoundException(f"Template for {username} with id {template_id} not found")

        return self._map_orm_to_template_entity(cast(ORMVisualizationTemplate, template))

    def get_user_templates(self, username: str) -> list[VisualizationTemplateEntity]:
        with self._db.session() as session:
            session: Session

            templates = (
                session.query(ORMVisualizationTemplate)
                .filter(ORMVisualizationTemplate.owner_username == username)
                .all()
            )

        return [
            self._map_orm_to_template_entity(cast(ORMVisualizationTemplate, template))
            for template in templates
        ]

    def save_template(self, username: str, template: VisualizationTemplateEntity) -> None:
        self._logger.info(f"[VisualizationTemplateRepository] Saving template for user {username}")

        with self._db.session() as session:
            session: Session

            session.add(
                ORMVisualizationTemplate(
                    name=template.name,
                    owner_username=username,
                    content_types=template.content_types,
                    visualization_diagram_types=template.visualization_diagram_types,
                )
            )

    def delete_template(self, template_id: int, username: str) -> None:
        with self._db.session() as session:
            session: Session

            template = (
                session.query(ORMVisualizationTemplate)
                .filter(
                    and_(
                        ORMVisualizationTemplate.id == template_id,
                        ORMVisualizationTemplate.owner_username == username,
                    )
                )
                .first()
            )

            if template is None:
                return

            session.delete(template)

    def update_template(self, template_id: int, username: str, template: VisualizationTemplateEntity) -> None:
        with self._db.session() as session:
            session: Session

            orm_template = (
                session.query(ORMVisualizationTemplate)
                .filter(
                    and_(
                        ORMVisualizationTemplate.id == template_id,
                        ORMVisualizationTemplate.owner_username == username,
                    )
                )
                .first()
            )

            if orm_template is None:
                raise UserTemplateNotFoundException(f"Template for {username} with id {template_id} not found")

            orm_template.name = template.name
            orm_template.content_types = template.content_types
            orm_template.visualization_diagram_types = template.visualization_diagram_types

    def _map_orm_to_template_entity(self, orm_template: ORMVisualizationTemplate) -> VisualizationTemplateEntity:
        return VisualizationTemplateEntity(
            id=orm_template.id,
            name=orm_template.name,
            content_types=orm_template.content_types,
            visualization_diagram_types=orm_template.visualization_diagram_types,
        )
