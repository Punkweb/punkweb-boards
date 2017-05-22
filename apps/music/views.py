from django.shortcuts import render, redirect

from . import models


def index_view(request):
    artists = models.Artist.objects.all()
    albums = models.Album.objects.all()
    audio = models.Audio.objects.all()
    compilations = models.AudioCompilation.objects.all()
    context = {
        'artists': artists,
        'albums': albums,
        'audio': audio,
        'compilations': compilations
    }
    return render(request, 'music/index.html', context)


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    return render(request, 'music/audio_view.html', context)


def audio_compilation_view(request, slug):
    compilation = models.AudioCompilation.objects.get(slug=slug)
    tracks = compilation.tracks
    context = {
        'compilation': compilation,
        'tracks': tracks
    }
    return render(request, 'music/audio_compilation_view.html', context)
