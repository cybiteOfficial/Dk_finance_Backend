# Generated by Django 4.2.11 on 2024-05-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_customerdetails_comment_customerdetails_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='customerSegment',
            field=models.CharField(choices=[('segment1', 'Segment 1'), ('segment2', 'Segment 2'), ('segment3', 'Segment 3')], max_length=255, null=True),
        ),
    ]