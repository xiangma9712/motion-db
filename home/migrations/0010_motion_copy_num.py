# Generated by Django 2.2.6 on 2019-11-06 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_tournament_ongoing'),
    ]

    operations = [
        migrations.AddField(
            model_name='motion',
            name='copy_num',
            field=models.IntegerField(default=0),
        ),
    ]