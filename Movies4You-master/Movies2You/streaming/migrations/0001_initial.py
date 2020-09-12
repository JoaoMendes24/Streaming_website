# Generated by Django 2.1.7 on 2019-04-29 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField(default=0)),
                ('movie_name', models.CharField(max_length=100)),
                ('movie_sinopse', models.CharField(max_length=1000)),
                ('movie_time', models.TimeField(verbose_name='movie time')),
                ('release_date', models.DateTimeField(verbose_name='release date')),
                ('movie_director', models.CharField(max_length=100)),
                ('movie_genre', models.CharField(max_length=100)),
                ('premium', models.BooleanField(default=False)),
                ('movie_score', models.IntegerField(default=0)),
            ],
        ),
    ]
