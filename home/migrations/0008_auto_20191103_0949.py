# Generated by Django 2.2.6 on 2019-11-03 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20191102_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='link_txt',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
