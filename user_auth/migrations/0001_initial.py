# Generated by Django 4.2.11 on 2024-04-21 13:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank_name', models.CharField(max_length=100)),
                ('branch_name', models.CharField(max_length=100)),
                ('ifsc_code', models.CharField(max_length=20, unique=True)),
                ('branch_code', models.CharField(max_length=20, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('country', models.CharField(default='India', max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=20)),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('description', models.TextField(null=True)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.comments')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('user_type', models.CharField(choices=[('ro', 'Ro'), ('do', 'Do'), ('technicalofficer', 'Technicalofficer'), ('bm', 'Bm'), ('md', 'MD'), ('cluster', 'Cluster')], max_length=250)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('otp', models.IntegerField(blank=True, null=True, validators=[validators.validate_otp_length])),
                ('aadhar_number', models.CharField(blank=True, max_length=12, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('bank_branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_auth.bankdetails')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
                'permissions': [('can_view', 'Can view'), ('can_change', 'Can change'), ('can_delete', 'Can delete')],
            },
        ),
    ]
