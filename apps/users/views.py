from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import render, redirect
from .models import EmailUser

def register_view(request):
    context = {}
    return render(request, 'board/register.html', context)

def my_profile(request):
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    context = {}
    return render(request, 'board/my_profile.html', context)

def settings_view(request):
    context = {}
    return render(request, 'board/settings.html', context)

def profile_view(request, username):
    user = EmailUser.objects.get(username=username)
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    if request.user.id == user.id:
        return redirect('board:me')
    context = {
        'profile': user
    }
    return render(request, 'board/profile_page.html', context)
