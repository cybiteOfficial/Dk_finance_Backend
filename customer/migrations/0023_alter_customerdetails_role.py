# Generated by Django 4.2.11 on 2024-07-01 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0022_alter_customerdetails_educationqualification_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerdetails",
            name="role",
            field=models.CharField(
                choices=[
                    ("applicant", "APPLICANT"),
                    ("co_applicant", "CO-APPLICANT"),
                    ("guarantor", "GUARANTOR"),
                ],
                max_length=255,
            ),
        ),
    ]