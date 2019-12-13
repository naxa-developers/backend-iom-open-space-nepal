# Generated by Django 2.2.7 on 2019-12-13 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20191212_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceDocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='openspace',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='resource',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource', to='core.ResourceCategory'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource', to='core.ResourceDocumentType'),
        ),
    ]