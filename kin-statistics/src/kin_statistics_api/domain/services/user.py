from kin_statistics_api.infrastructure.repositories import ReportsAccessManagementRepository


class UserService:
    def __init__(self, access_repository: ReportsAccessManagementRepository):
        self._access_repository = access_repository

    def count_user_reports_generations(self, username: str) -> int:
        return self._access_repository.count_user_reports_synchronous_generations(username=username)
