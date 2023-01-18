from django.test import Client, TestCase

from api.exceptions import ReportNotFound
from api.models import User
from api.tests.int import factories as fc
from api.tests.int.urls import APIUrls
from api.views import container
from kin_news_core.auth import create_jwt_token


class TestReportsService(TestCase):
    def setUp(self) -> None:
        self._user = User.objects.create_user("test", "test")
        report_id = container.repositories.reports_access_management_repository().create_new_user_report(self._user.id)

        self._test_report = fc.build_wordcloud_report(report_id)
        container.repositories.reports_repository().save_user_report(self._test_report)

        token = create_jwt_token(self._user.username)
        self._client = Client(HTTP_AUTHORIZATION=f'Token {token}')

    def test__get_user_reports_names(self):
        response = self._client.get(APIUrls.reports_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()['reports']

        self.assertEqual(len(data), 1)

        report = data[0]

        self.assertEqual(report["processingStatus"], "Ready")
        self.assertEqual(report["name"], self._test_report.name)
        self.assertEqual(report["reportId"], self._test_report.report_id)

    def test__get_detailed_report(self):
        response = self._client.get(APIUrls.report_details_url(self._test_report.report_id))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["reportId"], self._test_report.report_id)
        self.assertEqual(data["name"], self._test_report.name)

        response_dct = data['dataByChannel']

        for key in response_dct.keys():
            for word_freq1, word_freq2 in zip(response_dct[key], self._test_report.data_by_channel[key]):
                self.assertEqual(word_freq1[0], word_freq2[0])
                self.assertEqual(word_freq1[1], word_freq2[1])

    def test__updating_report_name(self):
        response = self._client.put(
            APIUrls.report_details_url(self._test_report.report_id),
            data={"name": "ANOTHER_NAME", "reportId": self._test_report.report_id},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        report = container.repositories.reports_repository().get_report(self._test_report.report_id)

        self.assertEqual(report.name, "ANOTHER_NAME")

    def test__delete_report(self):
        response = self._client.delete(APIUrls.report_details_url(self._test_report.report_id))

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ReportNotFound):
            container.repositories.reports_repository().get_report(self._test_report.report_id)
