# Generated by Django 3.0.2 on 2020-02-19 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20200216_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='asianset',
            name='theme',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 19, 16, 1, 25, 576417)),
        ),
    ]
