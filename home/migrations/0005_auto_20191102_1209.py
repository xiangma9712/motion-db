# Generated by Django 2.2.6 on 2019-11-02 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20191102_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='info',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='setting',
            name='str',
            field=models.CharField(default='', max_length=15),
        ),
    ]
