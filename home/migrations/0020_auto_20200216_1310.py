# Generated by Django 3.0.2 on 2020-02-16 04:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20200215_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 13, 10, 19, 950271)),
        ),
        migrations.AlterField(
            model_name='motion',
            name='fairness',
            field=models.IntegerField(default=2),
        ),
    ]