# Generated by Django 4.2.11 on 2024-07-03 19:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ErrorLog",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("error_type", models.CharField(max_length=255)),
                ("module", models.CharField(max_length=255)),
                ("pathname", models.CharField(max_length=1024)),
                ("lineno", models.IntegerField()),
                ("funcName", models.CharField(max_length=255)),
                ("error_message", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
