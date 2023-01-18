from django.contrib.auth.models import User

from api.models import UserGeneratesReport


class UserRepository:
    def __init__(self):
        self._user_query = User.objects
        self._user_generates_report_query = UserGeneratesReport.objects

    def check_if_username_exists(self, username: str) -> bool:
        return self._user_query.filter(username=username).exists()

    def create_user_by_username(self, username: str) -> None:
        self._user_query.create_user(username=username)

    def count_user_reports_generations(self, user_id: int) -> int:
        report_generating, _ = self._user_generates_report_query.get_or_create(user_id=user_id)

        return report_generating.reports_generated_count
