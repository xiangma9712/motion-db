# Generated by Django 2.2.6 on 2019-11-02 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20191102_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='info',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='str',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]
