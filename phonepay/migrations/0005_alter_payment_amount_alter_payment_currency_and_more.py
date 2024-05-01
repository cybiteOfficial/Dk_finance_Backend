# Generated by Django 4.2.11 on 2024-04-25 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_initial'),
        ('phonepay', '0004_payment_comment_payment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=5000.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='INR', max_length=3),
        ),
        migrations.AlterField(
            model_name='payment',
            name='lead_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lead', to='leads.leads'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('done', 'DONE'), ('pending', 'PENDING'), ('failed', 'FAILED')], default='Done', max_length=255),
        ),
    ]