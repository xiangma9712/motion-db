# Generated by Django 3.0.2 on 2020-02-16 08:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20200216_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 17, 12, 16, 872626)),
        ),
        migrations.AlterField(
            model_name='motion',
            name='meta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Meta'),
        ),
        migrations.CreateModel(
            name='AsianSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one', to='home.Motion')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Round')),
                ('three', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='three', to='home.Motion')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Tournament')),
                ('two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='two', to='home.Motion')),
            ],
        ),
    ]
