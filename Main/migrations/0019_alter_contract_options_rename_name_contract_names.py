# Generated by Django 5.0.4 on 2024-04-30 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0018_contract'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name': 'Contract sm'},
        ),
        migrations.RenameField(
            model_name='contract',
            old_name='name',
            new_name='names',
        ),
    ]
