from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from kin_statistics_api.constants import REPORTS_BUILDER_EXCHANGE, API_ROUTE_PATH
from kin_statistics_api.domain.entities import ReportIdentificationEntity, GenerateReportEntity
from kin_statistics_api.domain.events import GenerateReportRequestOccurred
from kin_statistics_api.infrastructure.dtos import ReportIdentitiesQueryResult


class TestReportsViews:
    def test_get_user_reports(
        self,
        test_http_client__unauthorized: TestClient,
        username_with_access_token_headers: tuple[str, dict[str, str]],
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        mock__access_management_repository.get_user_report_ids.return_value = [1]
        query_result = ReportIdentitiesQueryResult(
            reports=[
                ReportIdentificationEntity(
                    report_id=1,
                    name="report_name",
                    report_type="Statistical",
                    generation_date="01/01/2022 00:00",
                    processing_status="Ready",
                )
            ],
            total_reports=1,
        )

        mock__reports_repository.get_user_reports.return_value = query_result

        username, auth_headers = username_with_access_token_headers
        client = test_http_client__unauthorized
        response = client.get(
            f"{API_ROUTE_PATH}/reports?page=1&name=some_name&processingStatus=Ready",
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json() == {
            "data": [
                {
                    "reportId": 1,
                    "name": "report_name",
                    "reportType": "Statistical",
                    "generationDate": "01/01/2022 00:00",
                    "processingStatus": "Ready",
                    "reportFailedReason": None,
                    "reportWarnings": None,
                }
            ],
            "totalPages": 1,
            "page": 1,
        }

    def test_get_user_reports__no_reports(
        self,
        test_http_client__unauthorized: TestClient,
        username_with_access_token_headers: tuple[str, dict[str, str]],
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        mock__access_management_repository.get_user_report_ids.return_value = []
        mock__reports_repository.get_user_reports.return_value = ReportIdentitiesQueryResult(reports=[], total_reports=0)

        username, auth_headers = username_with_access_token_headers
        client = test_http_client__unauthorized

        response = client.get(f"{API_ROUTE_PATH}/reports", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == {
            "data": [],
            "totalPages": 0,
            "page": 0,
        }

    def test_generate_report_request(
        self,
        generate_report_entity: tuple[dict, GenerateReportEntity],
        test_http_client__unauthorized: TestClient,
        username_with_access_token_headers: tuple[str, dict[str, str]],
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
        mock__events_producer: MagicMock,
    ) -> None:
        report_id = 1
        mock__access_management_repository.create_new_user_report.return_value = report_id
        mock__access_management_repository.count_user_reports_synchronous_generations.return_value = 0

        json, entity = generate_report_entity
        username, auth_headers = username_with_access_token_headers
        client = test_http_client__unauthorized

        response = client.post(f"{API_ROUTE_PATH}/reports", json=json, headers=auth_headers)

        assert response.status_code == 202
        assert response.json() == {"message": "Generating report process started successfully!"}

        generation_event = GenerateReportRequestOccurred(
            **entity.dict(),
            username=username,
            report_id=report_id,
        )

        mock__events_producer.publish.assert_called_once_with(
            REPORTS_BUILDER_EXCHANGE,
            [generation_event],
        )

    def test_generate_report_request__too_many_reports(
        self,
        generate_report_entity: tuple[dict, GenerateReportEntity],
        test_http_client__unauthorized: TestClient,
        username_with_access_token_headers: tuple[str, dict[str, str]],
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        json, _ = generate_report_entity
        mock__access_management_repository.count_user_reports_synchronous_generations.return_value = 10

        username, auth_headers = username_with_access_token_headers
        client = test_http_client__unauthorized

        response = client.post(f"{API_ROUTE_PATH}/reports", json=json, headers=auth_headers)

        assert response.status_code == 409
        assert response.json() == {
            "errors": "Sorry, but you can not generate more than 3 at the same time"
        }
