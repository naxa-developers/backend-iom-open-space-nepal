# Generated by Django 2.2.6 on 2019-11-11 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20191107_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openspace',
            name='capacity',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=25, null=True),
        ),
        migrations.AlterField(
            model_name='openspace',
            name='total_area',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=25, null=True),
        ),
        migrations.AlterField(
            model_name='openspace',
            name='usable_area',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=25, null=True),
        ),
    ]