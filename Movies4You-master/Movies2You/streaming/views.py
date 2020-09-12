from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Movie
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from social_django.models import UserSocialAuth
import os.path
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    recent_movies = Movie.objects.order_by('-release_date')[:5]
    top_movies = Movie.objects.order_by('-movie_score')[:5]
    context = {'recent_movies': recent_movies, 'top_movies': top_movies}
    return render(request, 'streaming/index.html', context)


def catalog(request):
    all_movies = Movie.objects.order_by('-release_date')
    context = {'all_movies': all_movies}
    return render(request, 'streaming/catalog.html', context)


def movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'streaming/movie.html', {'movie': movie})


def movie_video(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'streaming/movie_video.html', {'movie': movie})


def movie_trailer(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'streaming/movie_trailer.html', {'movie': movie})


def premium(request):
    all_movies = Movie.objects.order_by('-release_date')
    context = {'all_movies': all_movies}
    return render(request, 'streaming/premium_catalog.html', context)


def search(request):
    name = request.POST['nome']
    genre = request.POST['genero']
    order = request.POST['order']
    all_movies = Movie.objects.all()
    if order == '1':
        all_movies = Movie.objects.order_by('-release_date')
    else:
        if order == '2':
            all_movies = Movie.objects.order_by('-movie_score')
    context = {'genre': genre, 'all_movies': all_movies, 'name': name}
    return render(request, 'streaming/search.html', context)


def searchpremium(request):
    name = request.POST['nome']
    genre = request.POST['genero']
    order = request.POST['order']
    all_movies = Movie.objects.all()
    if order == '1':
        all_movies = Movie.objects.order_by('-release_date')
    else:
        if order == '2':
            all_movies = Movie.objects.order_by('-movie_score')
    context = {'genre': genre, 'all_movies': all_movies, 'name': name}
    return render(request, 'streaming/searchpremium.html', context)


def register(request):
    context = {}
    return render(request, 'streaming/register.html', context)


def login(request):
    context = {'alerta': 1, }
    return render(request, 'streaming/login.html', context)


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect(request.GET.get('next', 'streaming:profile'))
    else:
        return render(request, 'streaming/login.html',
                      {'alerta': 0, 'error_message': "Incorrect username or password!", })


def registerview(request):
    name = request.POST['name']
    username = request.POST['username']
    email = request.POST['email']
    passw = request.POST['pass']
    try:
        user = User.objects.create_user(username, email, passw)
        user.first_name = name
        user.save()
        user.is_active = True
        send_mail('Movies2You - Welcome',
                  'Congratulations, ' + name + '! Now you are a registered user. You can watch lots of movies for free!\nGo to http://localhost:8000/streaming/ and have fun!\n\nYou username is: ' + username + '\nYour password is: ' + passw + '\n\n[Automatic Email. Do not answer it]\n\n\nMovies2You Team',
                  settings.EMAIL_HOST_USER, [email], fail_silently=False)
    except IntegrityError:
        return render(request, 'streaming/register.html', {'error_message': "User already exists!", })
    else:
        return HttpResponseRedirect(reverse('streaming:profile', ))


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('streaming:index', ))


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


@login_required(login_url='/streaming/login')
def profile(request, ):
    try:
        facebook_login = request.user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (request.user.social_auth.count() > 1 or request.user.has_usable_password())
    context = {'facebook_login': facebook_login, 'can_disconnect': can_disconnect}
    if request.method == 'POST' and 'profile_image' in request.FILES:
        image = request.FILES['profile_image']
        imageExt = os.path.splitext(image.name)[1]
        path = "users/" + str(request.user.id) + imageExt
        fs = OverwriteStorage()
        filename = fs.save(path, image)
        uploaded_file_url = fs.url(filename)
        request.user.utilizador.profile_img = uploaded_file_url
        request.user.save()
    elif request.method == 'POST':
        if 'new_passwd' in request.POST and 'new_passwd_conf' in request.POST:
            newPasswd = request.POST['new_passwd']
            newPasswdConf = request.POST['new_passwd_conf']
            if 'old_passwd' in request.POST:
                oldPasswd = request.POST['old_passwd']
                if not request.user.check_password(oldPasswd):
                    context.update({'message': "Incorrect password!", })
                    return render(request, 'streaming/profile.html', context)
            if newPasswdConf != newPasswd:
                context.update({'message': "The passwords didn't match!", })
            elif newPasswdConf != newPasswd:
                context.update({'message': "The passwords didn't match!", })
            elif newPasswd.strip() == '' or newPasswdConf.strip == '':
                context.update({'message': "Insert a valid password!", })
            else:
                request.user.set_password(newPasswd)
                request.user.save()
                context.update({'message': "New password successfully defined!", })
        elif 'cardnumber' in request.POST and 'cvv' in request.POST:
            request.user.utilizador.premium = True
            request.user.save()
            context.update({'message': "Congratulations! Now you are a premium user!", })
        elif 'first_name' in request.POST and not request.POST['first_name'].strip() == '':
            request.user.first_name = request.POST['first_name']
            request.user.save()
        if 'last_name' in request.POST and not request.POST['last_name'].strip() == '':
            request.user.last_name = request.POST['last_name']
            request.user.save()
        if 'email_add' in request.POST and not request.POST['email_add'].strip() == '':
            request.user.email = request.POST['email_add']
            request.user.save()
    return render(request, 'streaming/profile.html', context)
