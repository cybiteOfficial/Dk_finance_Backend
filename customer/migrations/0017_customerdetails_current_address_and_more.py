# Generated by Django 4.2.11 on 2024-05-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_remove_customerdetails_current_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='current_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='loan_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='occupation',
            field=models.CharField(blank=True, default='Worker', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='permanent_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
