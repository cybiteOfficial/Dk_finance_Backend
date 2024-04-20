# Generated by Django 4.2.11 on 2024-04-20 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lead_id', models.CharField(default='ld_042692', max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('agent_code', models.CharField(max_length=255, null=True)),
                ('branch_code', models.CharField(max_length=255, null=True)),
                ('branch_name', models.CharField(max_length=255, null=True)),
                ('loan_amount', models.CharField(max_length=255, null=True)),
                ('product_type', models.CharField(choices=[('normal', 'Normal')], default='normal', max_length=255)),
                ('case_tag', models.CharField(choices=[('normal', 'Normal')], default='normal', max_length=255)),
                ('customer_type', models.CharField(choices=[('home_loan', 'HomeLoan')], default='home_loan', max_length=255)),
                ('source', models.CharField(choices=[('website', 'Website'), ('out_source', 'Out_Source')], default='website', max_length=255)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='leads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
