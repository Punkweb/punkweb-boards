from django.shortcuts import render, redirect
from apps.board.settings import BOARD_THEME
from apps.pages.models import Page

def page_view(request, slug):
    if not slug:
        return redirect('board:index')
    if request.user.is_authenticated and request.user.is_banned:
        return redirect('board:unpermitted')
    page = Page.objects.get(slug=slug)
    context = {
        'page': page,
    }
    return render(
        request, 'board/themes/{}/page.html'.format(BOARD_THEME), context)
