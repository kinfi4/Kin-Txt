from kin_statistics_api.domain.entities.generation_template import GenerationTemplate
from kin_statistics_api.infrastructure.repositories.templates import TemplatesRepository


class GenerationTemplateService:
    def __init__(self, templates_repository: TemplatesRepository) -> None:
        self._templates_repository = templates_repository

    def get_user_template_names(self, username: str) -> list[dict[str, str]]:
        return self._templates_repository.get_user_template_names(username)

    def load_user_template(self, username: str, template_id: int) -> GenerationTemplate:
        return self._templates_repository.load_user_template(username, template_id)

    def save_user_template(self, username: str, template: GenerationTemplate) -> None:
        self._templates_repository.save_user_template(username, template)

    def delete_user_template(self, username: str, template_id: int) -> None:
        self._templates_repository.delete_template(username, template_id)
