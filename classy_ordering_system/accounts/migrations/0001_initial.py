# Generated by Django 3.0 on 2021-09-11 07:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('name', models.CharField(db_index=True, max_length=50, validators=[django.core.validators.RegexValidator(message='Please enter alphabets only', regex='^[a-z A-Z]+$')], verbose_name='Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('user_role', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Franchise'), (3, 'Employee'), (4, 'Production Center')], verbose_name='User Role')),
                ('company_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Company Name')),
                ('company_name2', models.CharField(blank=True, max_length=500, null=True, verbose_name='Company Name 2')),
                ('address', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Address')),
                ('suite_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Suite Number')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='State')),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Zip code')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('fax_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Fax Number')),
                ('license_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='License Number')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('tenent_id', models.SmallIntegerField(blank=True, null=True)),
                ('tenent_name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_employee', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='UserSecurityToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('extras', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.CharField(max_length=150)),
                ('token_type', models.SmallIntegerField(choices=[(1, 'Forgot Password'), (2, 'Account Activation Token')])),
                ('expire_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('page', models.CharField(blank=True, max_length=255, null=True)),
                ('feedback', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('client_id', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_feedback', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
                'db_table': 'feedbacks',
            },
        ),
    ]
