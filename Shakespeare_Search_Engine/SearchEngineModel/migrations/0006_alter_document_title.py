# Generated by Django 3.2 on 2021-04-14 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngineModel', '0005_document_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
