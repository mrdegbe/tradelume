# Generated by Django 5.2.1 on 2025-06-03 23:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tradelog",
            name="entry_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="tradelog",
            name="exit_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
