# Generated by Django 4.2.11 on 2024-04-23 03:37

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customerdetails_current_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerdetails',
            old_name='customer_segment',
            new_name='agriculturalLand',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='industry',
            new_name='customerSegment',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='dob',
            new_name='dateOfBirth',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='agent_code',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='branch_code',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='monthly_family_income',
            new_name='monthlyFamilyIncome',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='monthly_income',
            new_name='monthlyIncome',
        ),
        migrations.RenameField(
            model_name='customerdetails',
            old_name='source_of_income',
            new_name='sourceOfIncome',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='case_tag',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='customer_type',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='kyc_id',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='questions',
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='earningsFromAgriculturalLand',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='educationQualification',
            field=models.CharField(null=True, verbose_name=255),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='numberOfDependents',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='residenceOwnership',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='valueOfAgriculturalLand',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='cif_id',
            field=models.CharField(default=utils.generate_customerID, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='load_amount',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
