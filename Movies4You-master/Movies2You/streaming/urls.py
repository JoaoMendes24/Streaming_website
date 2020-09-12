from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.urls import path

app_name = 'streaming'

urlpatterns = [
                  # ex: /streaming/
                  url(r'^$', views.index, name='index'),
                  url(r'^catalog/$', views.catalog, name='catalog'),
                  url(r'^movie(?P<movie_id>[0-9]+)/$', views.movie, name='movie'),
                  url(r'^loginview/$', views.loginview, name='loginview'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^movie_trailer(?P<movie_id>[0-9]+)/$', views.movie_trailer, name='movie_trailer'),
                  url(r'^movie_video(?P<movie_id>[0-9]+)/$', views.movie_video, name='movie_video'),
                  url(r'^registerview/$', views.registerview, name='registerview'),
                  url(r'^premium/$', views.premium, name='premium'),
                  url(r'^profile/$', views.profile, name='profile'),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^logout/$', views.logoutview, name='logout'),
                  url(r'^/login/oauth/', include('social_django.urls', namespace='social')),
                  url(r'^search/$', views.search, name='search'),
                  url(r'searchpremium/$', views.searchpremium, name='searchpremium')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
