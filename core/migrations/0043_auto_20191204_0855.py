# Generated by Django 2.2.7 on 2019-12-04 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20191202_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedUseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_use', to='core.OpenSpace')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedUseList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('icon', models.FileField(blank=True, null=True, upload_to='suggest')),
            ],
        ),
        migrations.DeleteModel(
            name='SuggestedUse',
        ),
        migrations.AddField(
            model_name='suggestedusedata',
            name='suggested_use',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_use', to='core.SuggestedUseList'),
        ),
    ]
