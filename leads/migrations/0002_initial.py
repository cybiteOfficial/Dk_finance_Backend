# Generated by Django 4.2.11 on 2024-04-21 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='leads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leads',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.comments'),
        ),
    ]
