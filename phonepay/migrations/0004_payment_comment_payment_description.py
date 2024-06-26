# Generated by Django 4.2.11 on 2024-04-24 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
        ('phonepay', '0003_alter_payment_lead_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.comments'),
        ),
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
