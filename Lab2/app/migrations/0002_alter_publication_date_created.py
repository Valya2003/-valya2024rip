# Generated by Django 4.2.7 on 2024-09-22 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 16, 48, 59, 314522, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]