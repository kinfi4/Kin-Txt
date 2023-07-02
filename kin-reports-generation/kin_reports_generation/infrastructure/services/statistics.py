from typing import Optional, TextIO

from requests import JSONDecodeError

from kin_news_core.service_proxy import ServiceProxy, ServiceProxyError


class StatisticsService(ServiceProxy):
    def __init__(self, url: str, kin_token: Optional[str] = None, jwt_token: Optional[str] = None) -> None:
        super().__init__(jwt_token=jwt_token, kin_token=kin_token)
        self._base_url = url

    def save_report_data(self, report_id: int, file_type: str, data: TextIO) -> None:
        self._logger.info(f'Saving data for processed report={report_id} in statistics service...')

        target_url = f'{self._base_url}/reports-data/save'
        response = self._session.post(
            url=target_url,
            files={'report_data_file': data},
            data={'report_id': report_id, 'file_type': file_type},
        )

        if not response.ok:
            try:
                message = response.json()
            except JSONDecodeError:
                message = response.text

            self._logger.error(
                f'[StatisticsService] '
                f'Request to {target_url} failed with status: {response.status_code} with message: {message}.'
            )

            raise ServiceProxyError(f'Request to {target_url} failed with status: {response.status_code}')
