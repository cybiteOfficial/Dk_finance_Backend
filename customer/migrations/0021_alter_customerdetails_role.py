# Generated by Django 4.2.11 on 2024-06-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0020_alter_customerdetails_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerdetails",
            name="role",
            field=models.CharField(
                choices=[("applicant", "APPLICANT"), ("co_applicant", "CO-APPLICANT")],
                max_length=255,
            ),
        ),
    ]
