# Generated by Django 4.2.11 on 2024-06-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0003_alter_leads_agent_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leads",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]