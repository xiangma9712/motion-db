# Generated by Django 3.0.2 on 2020-02-16 05:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20200216_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='motion',
            name='round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Round'),
        ),
        migrations.AddField(
            model_name='motion',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Tournament'),
        ),
        migrations.AddField(
            model_name='motion',
            name='year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 14, 27, 4, 328240)),
        ),
    ]
