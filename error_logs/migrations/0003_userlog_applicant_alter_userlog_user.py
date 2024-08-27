# Generated by Django 4.2.11 on 2024-07-05 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("applicants", "0014_alter_applicants_application_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("error_logs", "0002_userlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="userlog",
            name="applicant",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="applicants.applicants",
            ),
        ),
        migrations.AlterField(
            model_name="userlog",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
