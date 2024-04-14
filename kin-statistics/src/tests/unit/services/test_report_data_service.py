import os
from unittest.mock import MagicMock, mock_open

import pytest

from kin_statistics_api.domain.entities import User
from kin_statistics_api.domain.services.report_data import JsonFileGenerator, CsvFileGenerator, ReportDataSaver
from kin_statistics_api.exceptions import ReportDataNotFound


class TestJsonFileGenerator:

    def test_get_file(
        self,
        json_file_generator: JsonFileGenerator,
        mock__access_management_repository: MagicMock,
        mocker: MagicMock,
    ) -> None:
        # Arrange
        user = User(username="test-username")
        report_id = 1

        mock__access_management_repository.get_user_report_ids.return_value = [report_id]
        mocker.patch("builtins.open", mock_open(read_data="read"))

        # Act
        result = json_file_generator.get_file(user, report_id)

        # Assert
        assert result[1] == f"report-{report_id}.json"

    def test_get_file_not_found(self, json_file_generator: JsonFileGenerator, mocker: MagicMock) -> None:
        # Arrange
        user = User(username="test-username")
        report_id = 1
        mocker.patch('builtins.open', side_effect=FileNotFoundError())

        # Act & Assert
        with pytest.raises(ReportDataNotFound):
            json_file_generator.get_file(user, report_id)


class TestCsvFileGenerator:

    def test_get_file(
        self,
        csv_file_generator: CsvFileGenerator,
        mock__access_management_repository: MagicMock,
        mocker: MagicMock,
    ) -> None:
        # Arrange
        user = User(username="test-username")
        report_id = 1

        mock__access_management_repository.get_user_report_ids.return_value = [report_id]
        mocker.patch('builtins.open', mock_open(read_data='data'))

        # Act
        result = csv_file_generator.get_file(user, report_id)

        # Assert
        assert result[1] == f"report-{report_id}.csv"

    def test_get_file_not_found(self, csv_file_generator: CsvFileGenerator, mocker: MagicMock) -> None:
        # Arrange
        user = User(username="test-username")
        report_id = 1
        mocker.patch('builtins.open', side_effect=FileNotFoundError())

        # Act & Assert
        with pytest.raises(ReportDataNotFound):
            csv_file_generator.get_file(user, report_id)


class TestReportDataSaver:

    def test_save_report_data(self, reports_data_saver: ReportDataSaver, mocker: MagicMock) -> None:
        # Arrange
        report_id = 1
        file_type = "csv"
        data_file = MagicMock()

        mocked_open = mocker.patch("builtins.open", mock_open())

        # Act
        reports_data_saver.save_report_data(report_id, file_type, data_file)

        expected_report_path = os.path.join(os.getenv("USER_REPORTS_FOLDER_PATH"), "1.csv")
        mocked_open.assert_called_once_with(expected_report_path, "wb")

    def test_save_report_data_invalid_file_type(self, reports_data_saver: ReportDataSaver) -> None:
        # Arrange
        report_id = 1
        file_type = "txt"
        data_file = MagicMock()

        # Act & Assert
        with pytest.raises(ValueError):
            reports_data_saver.save_report_data(report_id, file_type, data_file)
