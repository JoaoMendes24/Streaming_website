# Generated by Django 2.1.7 on 2019-04-29 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0003_auto_20190429_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_img',
            field=models.URLField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_video',
            field=models.URLField(default=0),
        ),
    ]
