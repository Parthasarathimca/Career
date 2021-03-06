# Generated by Django 3.0 on 2021-09-11 07:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('category_code', models.BigIntegerField(blank=True, null=True)),
                ('category_description', models.CharField(blank=True, max_length=255, null=True)),
                ('H1', models.CharField(blank=True, max_length=255, null=True)),
                ('W1', models.CharField(blank=True, max_length=255, null=True)),
                ('D1', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name': 'Category Code Map',
                'verbose_name_plural': 'Category Codes Map',
                'db_table': 'category_code_map',
            },
        ),
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('job_id', models.BigIntegerField(unique=True)),
                ('job_description', models.CharField(blank=True, max_length=255, null=True)),
                ('client_id', models.BigIntegerField()),
                ('client_name', models.CharField(blank=True, max_length=255, null=True)),
                ('order_status', models.CharField(choices=[('SENT', 'Orders Sent'), ('INPROGRESS', 'Orders Inprogress')], default='INPROGRESS', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('job_install_start_date', models.DateTimeField(blank=True, null=True, verbose_name='install_start_date')),
                ('job_install_end_date', models.DateTimeField(blank=True, null=True, verbose_name='install_end_date')),
                ('job_updated_at', models.DateTimeField(blank=True, null=True, verbose_name='job_updated_at')),
                ('designer', models.CharField(blank=True, max_length=255, null=True)),
                ('is_project_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_job', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='ProductionCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('production_center_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Production Center',
                'verbose_name_plural': 'Production Centers',
                'db_table': 'production_center',
            },
        ),
        migrations.CreateModel(
            name='RoomColorChoiceModelMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('color', models.CharField(max_length=400)),
                ('color_code', models.BigIntegerField(blank=True, null=True)),
                ('flat', models.BooleanField(default=False)),
                ('round', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='color_pics')),
            ],
            options={
                'verbose_name': 'Room Color Choice Map',
                'verbose_name_plural': 'Room Color Choices Map',
                'db_table': 'room_colors_choice_map',
            },
        ),
        migrations.CreateModel(
            name='RoomEdgeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('edge_type_code', models.BigIntegerField()),
                ('edge_type_text', models.CharField(max_length=255)),
                ('color', models.ManyToManyField(related_name='edge_type_color', to='franchise.RoomColorChoiceModelMap')),
            ],
            options={
                'verbose_name': 'Room Edge Type Map',
                'verbose_name_plural': 'Room Edge Types Map',
                'db_table': 'room_edge_type_map',
            },
        ),
        migrations.CreateModel(
            name='RoomMatTypeModelMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('mat_code', models.BigIntegerField()),
                ('mat_description', models.TextField(max_length=255)),
                ('size', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('color', models.ManyToManyField(related_name='mat_type_color', to='franchise.RoomColorChoiceModelMap')),
            ],
            options={
                'verbose_name': 'Room Material Type Map',
                'verbose_name_plural': 'Room Material Types Map',
                'db_table': 'room_material_type_map',
            },
        ),
        migrations.CreateModel(
            name='RoomProfileModelMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('profile_code', models.BigIntegerField()),
                ('profile_text', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Room Profile Map',
                'verbose_name_plural': 'Room Profiles Map',
                'db_table': 'room_profile_map',
            },
        ),
        migrations.CreateModel(
            name='RoomStainColorChoiceModelMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('sort', models.BigIntegerField(blank=True, null=True)),
                ('color', models.CharField(max_length=400)),
                ('color_code', models.BigIntegerField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='stain_pics')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Room Stain Color Map',
                'verbose_name_plural': 'Room Stain Color Choices Map',
                'db_table': 'room_stain_colors_choice_map',
            },
        ),
        migrations.CreateModel(
            name='RoomModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('room_name', models.CharField(max_length=255)),
                ('room_key', models.CharField(blank=True, max_length=255, null=True)),
                ('job_created_at', models.DateTimeField(blank=True, null=True, verbose_name='Create at')),
                ('order_status', models.CharField(choices=[('SENT', 'Orders Sent'), ('INPROGRESS', 'Orders Inprogress')], default='INPROGRESS', max_length=20)),
                ('bd_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_bd_color', to='franchise.RoomColorChoiceModelMap')),
                ('dd_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_color', to='franchise.RoomColorChoiceModelMap')),
                ('dd_ed_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_ed_color', to='franchise.RoomColorChoiceModelMap')),
                ('dd_ed_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_ed_profile', to='franchise.RoomProfileModelMap')),
                ('dd_ed_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_ed_type', to='franchise.RoomEdgeType')),
                ('dd_mat_color_stain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_mat_stain', to='franchise.RoomStainColorChoiceModelMap')),
                ('dd_mat_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_dd_mat_type', to='franchise.RoomMatTypeModelMap')),
                ('ed_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_ed_color', to='franchise.RoomColorChoiceModelMap')),
                ('ed_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_ed_profile', to='franchise.RoomProfileModelMap')),
                ('ed_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_ed_type', to='franchise.RoomEdgeType')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_room', to='franchise.JobModel')),
                ('mat_color_stain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_mat_color_stain', to='franchise.RoomStainColorChoiceModelMap')),
                ('mat_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_mat_type', to='franchise.RoomMatTypeModelMap')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
                'db_table': 'room',
            },
        ),
        migrations.AddField(
            model_name='roommattypemodelmap',
            name='color_stain',
            field=models.ManyToManyField(blank=True, null=True, related_name='mat_type_stain_color', to='franchise.RoomStainColorChoiceModelMap'),
        ),
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Modify Date')),
                ('job_status_id', models.IntegerField(blank=True, null=True)),
                ('order_send_time', models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 11, 13, 5, 30, 852917), null=True)),
                ('production_status', models.CharField(blank=True, max_length=100, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_status', to='franchise.JobModel')),
                ('production_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_production_center', to='franchise.ProductionCenter')),
            ],
            options={
                'verbose_name': 'Job Status',
                'verbose_name_plural': 'Jab Status',
                'db_table': 'job_status_master',
            },
        ),
    ]
