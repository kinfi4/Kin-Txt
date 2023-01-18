from django.contrib.auth.models import User
from django.db import models


class UserReport(models.Model):
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    report_id = models.PositiveIntegerField()

    def __str__(self):
        return str(self.report_id)


class UserGeneratesReport(models.Model):
    user = models.OneToOneField(User, related_name='report_generating', on_delete=models.CASCADE)
    reports_generated_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - generating: {self.report_is_generating}'
