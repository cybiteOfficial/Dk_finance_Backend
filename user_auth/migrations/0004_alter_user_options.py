# Generated by Django 4.2.11 on 2024-04-20 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_view', 'Can view'), ('can_change', 'Can change'), ('can_delete', 'Can delete')]},
        ),
    ]