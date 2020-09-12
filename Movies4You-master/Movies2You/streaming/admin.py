from django.contrib import admin
from .models import Movie, Utilizador
# Register your models here.

admin.site.site_url = '/streaming/'

admin.site.register(Movie)
admin.site.register(Utilizador)
