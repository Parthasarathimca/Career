# Generated by Django 3.0 on 2021-08-06 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_options', '0009_adjedge_adjinsertbacking_adjmaterial_adjwidth_ajddepth'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomoptionsmastermodel',
            name='adj_insert_backing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adj_shelf_insert_backing', to='room_options.AdjInsertBacking'),
        ),
        migrations.AddField(
            model_name='roomoptionsmastermodel',
            name='adj_shelf_edge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adj_shelf_edge', to='room_options.AdjEdge'),
        ),
    ]