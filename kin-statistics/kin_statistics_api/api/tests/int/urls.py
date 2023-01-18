from django.urls import reverse


class APIUrls:
    reports_url = reverse('reports')

    @staticmethod
    def report_details_url(report_id):
        return reverse('reports-single', args=(report_id,))
