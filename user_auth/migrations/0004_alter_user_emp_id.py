# Generated by Django 4.2.11 on 2024-06-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0003_user_emp_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="emp_id",
            field=models.CharField(null=True),
        ),
    ]
