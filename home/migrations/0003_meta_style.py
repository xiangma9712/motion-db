# Generated by Django 2.2.6 on 2019-11-01 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20191031_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='style',
            field=models.IntegerField(null=True),
        ),
    ]