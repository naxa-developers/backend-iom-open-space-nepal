# Generated by Django 2.2.7 on 2019-11-29 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_availablefacility_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openspace',
            name='elevation',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
    ]