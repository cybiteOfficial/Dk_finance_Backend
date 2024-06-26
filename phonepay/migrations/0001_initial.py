# Generated by Django 4.2.11 on 2024-04-22 16:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leads', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_id', models.CharField(max_length=255, unique=True)),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('status', models.CharField(choices=[('done', 'DONE'), ('pending', 'PENDING'), ('failed', 'FAILED')], max_length=255)),
                ('lead_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applicants', to='leads.leads')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
