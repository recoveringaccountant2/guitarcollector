# Generated by Django 4.0.1 on 2022-01-27 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guitar',
            old_name='age',
            new_name='year',
        ),
    ]