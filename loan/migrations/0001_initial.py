# Generated by Django 4.2.11 on 2024-04-23 16:10

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicants', '0006_alter_applicants_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(default=utils.generate_locanID, max_length=255, unique=True)),
                ('product_type', models.CharField(max_length=255)),
                ('transaction_type', models.CharField(max_length=255)),
                ('case_tag', models.CharField(max_length=255)),
                ('applied_loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('applied_tenure', models.IntegerField()),
                ('applied_ROI', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(null=True)),
                ('remark', models.TextField(null=True)),
                ('processing_fees', models.JSONField(null=True)),
                ('valuation_charges', models.JSONField(null=True)),
                ('legal_and_incidental_fee', models.JSONField(null=True)),
                ('stamp_duty_applicable_rate', models.JSONField(null=True)),
                ('rcu_charges_applicable_rate', models.JSONField(null=True)),
                ('stamping_expenses_applicable_rate', models.JSONField(null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Applicant', to='applicants.applicants')),
            ],
        ),
    ]
