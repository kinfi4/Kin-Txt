import datetime
from unittest.mock import MagicMock

import pytest

from kin_statistics_api.domain.entities import (
    GenerateReportEntity,
    User,
    ReportsFetchSettings,
    ReportIdentificationEntity,
)
from kin_statistics_api.domain.services.report import ManagingReportsService
from kin_statistics_api.constants import ReportProcessingResult
from kin_statistics_api.exceptions import ReportAccessForbidden


class TestManagingReportsService:

    def test_report_processing_finished(
        self,
        reports_service: ManagingReportsService,
        mock__access_management_repository: MagicMock,
        mock__reports_repository: MagicMock,
    ) -> None:
        username = "test-username"
        report = MagicMock()

        reports_service.report_processing_finished(username, report)

        mock__access_management_repository.update_user_simultaneous_reports_generation.assert_called_once_with(username, -1)
        mock__reports_repository.save_finished_report.assert_called_once_with(report)

    def test_start_report_generation(
        self,
        reports_service: ManagingReportsService,
        mock__access_management_repository: MagicMock,
        mock__reports_repository: MagicMock,
        mock__events_producer: MagicMock,
    ) -> None:
        user = User(username="test-username")
        generation_entity = GenerateReportEntity(name="test_report", reportType="Statistical", modelCode="test_report", templateId=5, startDate="01/01/2022", endDate="01/02/2022", modelType="Sklearn Model", channels=["channel1", "channel2"])

        reports_service.start_report_generation(user, generation_entity)

        mock__access_management_repository.update_user_simultaneous_reports_generation.assert_called_once_with(user.username, 1)
        mock__reports_repository.create_user_report.assert_called_once()
        mock__events_producer.publish.assert_called_once()

    def test_update_report_status(
        self,
        reports_service: ManagingReportsService,
        mock__reports_repository: MagicMock,
    ) -> None:
        report_id = 1
        new_status = ReportProcessingResult.NEW

        reports_service.update_report_status(report_id, new_status)

        mock__reports_repository.update_report_status.assert_called_once_with(report_id, new_status)

    def test_get_user_reports_names(
        self,
        reports_service: ManagingReportsService,
        mock__reports_repository: MagicMock,
    ) -> None:
        username = "test-username"
        fetch_settings = ReportsFetchSettings(page=1, items_per_page=10)

        reports_service.get_user_reports_names(username, fetch_settings)

        mock__reports_repository.get_user_reports.assert_called_once_with(username, fetch_settings=fetch_settings)

    def test_set_report_name__without_access(
        self,
        reports_service: ManagingReportsService,
    ) -> None:
        username = "test-username"
        report_name = "new_report_name"
        report_id = 1

        with pytest.raises(ReportAccessForbidden):
            reports_service.set_report_name(username, report_name, report_id)

    def test_set_report_name__with_access(
        self,
        reports_service: ManagingReportsService,
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username = "test-username"
        report_name = "new_report_name"
        report_id = 1

        mock__access_management_repository.get_user_report_ids.return_value = [report_id, 2, 3]
        mock__reports_repository.update_report_name.return_value = ReportIdentificationEntity(
            report_id=report_id,
            name=report_name,
            processing_status=ReportProcessingResult.NEW,
            generation_date=datetime.datetime.now(),
        )

        result = reports_service.set_report_name(username, report_name, report_id)

        mock__reports_repository.update_report_name.assert_called_once_with(report_id, report_name)

        assert result.report_id == report_id
        assert result.name == report_name

    def test_get_user_detailed_report__with_access(
        self,
        reports_service: ManagingReportsService,
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username = "test-username"
        report_id = 1

        mock__access_management_repository.get_user_report_ids.return_value = [report_id, 2, 3]

        reports_service.get_user_detailed_report(username, report_id)

        mock__reports_repository.get_report.assert_called_once_with(report_id)

    def test_delete_report(
        self,
        reports_service: ManagingReportsService,
        mock__reports_repository: MagicMock,
        mock__access_management_repository: MagicMock,
    ) -> None:
        username = "test-username"
        report_id = 1
        mock__access_management_repository.get_user_report_ids.return_value = [report_id, 2, 3]

        reports_service.delete_report(username, report_id)

        mock__reports_repository.delete_report.assert_called_once_with(report_id=report_id)
