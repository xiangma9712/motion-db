# Generated by Django 3.0.2 on 2020-02-15 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20200211_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 23, 6, 13, 239366)),
        ),
    ]
