# Generated by Django 4.2.11 on 2024-06-28 09:53

from django.db import migrations, models
import utils


class Migration(migrations.Migration):
    dependencies = [
        ("applicants", "0013_applicants_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicants",
            name="application_id",
            field=models.CharField(
                default=utils.generate_applicationID, max_length=255, unique=True
            ),
        ),
    ]
