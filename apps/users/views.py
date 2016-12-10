from django.http import Http404
from django.shortcuts import render, redirect
from .models import EmailUser


def my_profile(request):
    try:
        user = request.user
        context = {
            'user': user
        }
    except:
        raise Http404('EmailUser does not exist')
    return render(request, 'users/my_profile.html', context)


def settings_view(request):
    try:
        user = request.user
        context = {
            'user': user
        }
    except:
        raise Http404('User does not exist')
    return render(request, 'users/settings.html', context)


def profile_view(request, user_id):
    try:
        user = EmailUser.objects.get(id=user_id)
        if request.user.id == user.id:
            return redirect('users:me')
        context = {
            'user': user
        }
    except:
        raise Http404('User does not exist')
    return render(request, 'users/profile_page.html', context)
