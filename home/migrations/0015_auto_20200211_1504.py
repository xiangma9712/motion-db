# Generated by Django 3.0.2 on 2020-02-11 06:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20191125_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 11, 15, 4, 5, 642527)),
        ),
        migrations.AlterField(
            model_name='motion',
            name='info_text',
            field=models.CharField(blank=True, default='', max_length=1500),
        ),
        migrations.AlterField(
            model_name='motion',
            name='theme_add',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='motion',
            name='theme_top',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
    ]
