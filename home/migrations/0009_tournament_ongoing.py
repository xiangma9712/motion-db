# Generated by Django 2.2.6 on 2019-11-03 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20191103_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='ongoing',
            field=models.BooleanField(default=True),
        ),
    ]
