# Generated by Django 4.1.2 on 2023-01-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_usergeneratesreport_user_alter_userreport_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergeneratesreport',
            name='report_is_generating',
        ),
        migrations.AddField(
            model_name='usergeneratesreport',
            name='reports_generated_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]