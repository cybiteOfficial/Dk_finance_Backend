# Generated by Django 4.2.11 on 2024-04-23 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_customerdetails_earningsfromagriculturalland_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='dateOfBirth',
            field=models.CharField(),
        ),
    ]
