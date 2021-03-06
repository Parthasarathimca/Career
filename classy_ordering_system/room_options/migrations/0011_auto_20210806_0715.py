# Generated by Django 3.0 on 2021-08-06 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_options', '0010_auto_20210806_0708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adjedge',
            old_name='adj_edge',
            new_name='edge',
        ),
        migrations.RenameField(
            model_name='adjedge',
            old_name='adj_edge_text',
            new_name='edge_text',
        ),
        migrations.RenameField(
            model_name='adjinsertbacking',
            old_name='adj_backing_size',
            new_name='backing_size',
        ),
        migrations.RenameField(
            model_name='adjinsertbacking',
            old_name='adj_backing_text',
            new_name='backing_text',
        ),
        migrations.RenameField(
            model_name='adjmaterial',
            old_name='adj_material',
            new_name='material',
        ),
        migrations.RenameField(
            model_name='adjmaterial',
            old_name='adj_material_text',
            new_name='material_text',
        ),
        migrations.RenameField(
            model_name='adjwidth',
            old_name='adj_width',
            new_name='width',
        ),
        migrations.RenameField(
            model_name='adjwidth',
            old_name='adj_width_text',
            new_name='width_text',
        ),
        migrations.RenameField(
            model_name='ajddepth',
            old_name='adj_depth',
            new_name='depth',
        ),
        migrations.RenameField(
            model_name='ajddepth',
            old_name='adj_depth_text',
            new_name='depth_text',
        ),
    ]
