# Generated by Django 4.2.11 on 2024-05-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_alter_customerdetails_customersegment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='customerSegment',
            field=models.CharField(max_length=255, null=True),
        ),
    ]