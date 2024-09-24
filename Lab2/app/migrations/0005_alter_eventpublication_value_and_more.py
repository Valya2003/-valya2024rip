# Generated by Django 4.2.7 on 2024-09-22 16:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_publication_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpublication',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='Поле м-м'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 16, 50, 43, 156648, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]