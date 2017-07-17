from django.shortcuts import render, redirect

from apps.board.settings import BOARD_THEME
from apps.api.models import Report
from . import models


def base_context(request):
    ctx = {}
    if request.user.is_authenticated and not request.user.is_banned:
        ctx.update({
            'notifications': request.user.notifications.all()[:5]
        })
        ctx.update({
            'unread_conversations': request.user.unread_conversations.count()
        })
        ctx.update({
            'unread_notifications': request.user.notifications.filter(read=False).count()
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
