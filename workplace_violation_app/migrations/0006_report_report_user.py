# Generated by Django 4.2.10 on 2024-03-20 22:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workplace_violation_app', '0005_report_delete_anonreportinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
