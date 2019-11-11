# Generated by Django 2.2.6 on 2019-11-07 12:01

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_province_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='boundary',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='district',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='municipality',
            name='boundary',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='municipality',
            name='hlcit_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='openspace',
            name='ward',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Ward',
        ),
    ]