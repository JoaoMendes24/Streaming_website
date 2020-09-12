from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_sinopse = models.CharField(max_length=1000)
    movie_time = models.CharField(max_length=50)
    release_date = models.DateTimeField('release date')
    movie_director = models.CharField(max_length=100)
    movie_genre = models.CharField(max_length=100)
    premium = models.BooleanField(default=False)
    movie_score = models.IntegerField(default=0)  # score vai de 0 a 10
    movie_img = models.URLField(default=0)
    movie_video = models.URLField(default=0)
    movie_trailer = models.URLField(default=0)

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    premium = models.BooleanField(default=False)
    profile_img = models.URLField(default= settings.MEDIA_URL + 'users/default.png')

    @receiver(post_save, sender=User)
    def create_user_utilizador(sender, instance, created, **kwargs):
        if created:
            Utilizador.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_utilizador(sender, instance, **kwargs):
        instance.utilizador.save()

# Create your models here.
