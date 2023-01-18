from kin_news_core.service_proxy import ServiceProxy


class StatisticsServiceProxy(ServiceProxy):
    def __init__(
        self,
        statistics_service_url: str,
        kin_token: str,
    ):
        super().__init__(kin_token=kin_token)
        self._statistics_service_url = statistics_service_url

    def send_create_user_request(self, username: str) -> None:
        self.post(f'{self._statistics_service_url}/api/v1/users', data={'username': username, 'token': self._kin_token})
