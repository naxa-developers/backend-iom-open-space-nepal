# Generated by Django 2.2.7 on 2019-12-18 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_auto_20191216_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='gallery_update',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
