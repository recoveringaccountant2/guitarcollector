# Generated by Django 4.0.1 on 2022-01-27 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_restring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restring',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='restring',
            name='date',
            field=models.DateField(verbose_name='restring date'),
        ),
    ]
