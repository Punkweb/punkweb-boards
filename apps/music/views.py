from django.shortcuts import render, redirect

from . import models


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    return render(request, 'music/audio_view.html', context)
