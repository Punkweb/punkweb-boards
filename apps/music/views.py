from django.shortcuts import render, redirect

from apps.board.settings import BOARD_THEME
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
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/music/index.html'.format(BOARD_THEME),
        context
    )


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/music/audio_view.html'.format(BOARD_THEME),
        context
    )


def audio_compilation_view(request, slug):
    compilation = models.AudioCompilation.objects.get(slug=slug)
    tracks = compilation.tracks
    context = {
        'compilation': compilation,
        'tracks': tracks
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/music/audio_compilation_view.html'.format(BOARD_THEME),
        context
    )
