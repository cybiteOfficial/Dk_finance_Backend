# Generated by Django 4.2.11 on 2024-04-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collateral_details', '0002_remove_collateraldetails_remark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collateraldetails',
            name='isExisting',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
