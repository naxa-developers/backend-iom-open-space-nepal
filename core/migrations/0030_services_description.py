# Generated by Django 2.2.7 on 2019-11-26 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_provincedummy'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]