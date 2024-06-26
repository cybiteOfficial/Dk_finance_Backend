# Generated by Django 4.2.11 on 2024-04-21 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicants', '0002_initial'),
        ('user_auth', '0001_initial'),
        ('kyc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kycdetails',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.comments'),
        ),
        migrations.AddField(
            model_name='documentsupload',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='application', to='applicants.applicants'),
        ),
        migrations.AddField(
            model_name='documentsupload',
            name='kyc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kyc_details', to='kyc.kycdetails'),
        ),
    ]
