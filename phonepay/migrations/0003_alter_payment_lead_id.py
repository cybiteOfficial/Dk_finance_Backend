# Generated by Django 4.2.11 on 2024-04-23 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_initial'),
        ('phonepay', '0002_alter_payment_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='lead_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lead', to='leads.leads'),
        ),
    ]