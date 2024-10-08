# Generated by Django 4.2.11 on 2024-06-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loan", "0004_alter_loan_transaction_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("purchase", "Purchase"),
                    ("refinance", "Refinance"),
                    ("construction", "Construction"),
                ],
                default="purchase",
                max_length=255,
                null=True,
            ),
        ),
    ]
