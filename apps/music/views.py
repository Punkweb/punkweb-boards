from django.shortcuts import render, redirect

from apps.api.models import Conversation, Report
from . import models


def base_context(request):
    ctx = {}
    if request.user.is_authenticated and not request.user.is_banned:
        ctx.update({
            'unread_conversations': request.user.unread_conversations.count()
        })
        if request.user.is_staff:
            unresolved_reports = Report.objects.filter(resolved=False).count()
            ctx.update({'unresolved_reports': unresolved_reports})
    return ctx


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
    return render(request, 'music/index.html', context)


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    context.update(base_context(request))
    return render(request, 'music/audio_view.html', context)


def audio_compilation_view(request, slug):
    compilation = models.AudioCompilation.objects.get(slug=slug)
    tracks = compilation.tracks
    context = {
        'compilation': compilation,
        'tracks': tracks
    }
    context.update(base_context(request))
    return render(request, 'music/audio_compilation_view.html', context)
