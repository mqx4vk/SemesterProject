# Generated by Django 4.2.10 on 2024-03-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workplace_violation_app', '0009_alter_report_report_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_number',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
