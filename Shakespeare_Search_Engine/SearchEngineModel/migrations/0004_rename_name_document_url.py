# Generated by Django 3.2 on 2021-04-13 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngineModel', '0003_alter_dictionary_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='name',
            new_name='url',
        ),
    ]
