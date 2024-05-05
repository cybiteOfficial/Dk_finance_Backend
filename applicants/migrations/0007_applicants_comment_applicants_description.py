# Generated by Django 4.2.11 on 2024-04-24 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
        ('applicants', '0006_alter_applicants_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicants',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.comments'),
        ),
        migrations.AddField(
            model_name='applicants',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
