# Generated by Django 4.2.11 on 2024-06-23 02:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="emp_id",
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
