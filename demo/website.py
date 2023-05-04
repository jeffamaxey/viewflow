from django.urls import path
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def users(request):
    return {
        'users': User.objects.filter(is_active=True).order_by('-username')
    }


def login_as(request):
    user = None

    if user_pk := request.GET.get('user_pk', None):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            pass

    if username := request.GET.get('username', None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    else:
        logout(request)

    redirect_to = request.GET.get('next')
    return (
        HttpResponseRedirect(redirect_to)
        if redirect_to
        else redirect('/workflow/')
    )


urlpatterns = [
    path('login_as/', login_as, name="login_as")
]
