# Generated by Django 2.2.7 on 2019-11-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191118_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('replied', 'REPLIED')], default='pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='report',
            name='urgency',
            field=models.CharField(choices=[('high', 'HIGH'), ('medium', 'MEDIUM'), ('low', 'LOW')], default='high', max_length=15),
        ),
    ]