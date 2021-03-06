# Generated by Django 2.2.6 on 2019-10-30 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('round', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_str', models.CharField(max_length=10)),
                ('is_preliminary', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_str', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_name', models.CharField(max_length=30)),
                ('style', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motion_text', models.CharField(max_length=1000)),
                ('info_text', models.CharField(max_length=1500)),
                ('theme_top', models.CharField(max_length=20)),
                ('theme_add', models.CharField(max_length=20)),
                ('meta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Meta')),
            ],
        ),
        migrations.AddField(
            model_name='meta',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Tournament'),
        ),
    ]
