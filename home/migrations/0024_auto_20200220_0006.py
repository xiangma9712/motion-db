# Generated by Django 3.0.2 on 2020-02-19 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20200219_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 20, 0, 6, 56, 575007)),
        ),
        migrations.AlterField(
            model_name='motion',
            name='fairness',
            field=models.FloatField(default=2),
        ),
    ]
