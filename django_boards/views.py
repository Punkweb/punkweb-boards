from django.shortcuts import render

from apps.board.settings import BOARD_THEME

def portal_view(request):
    context = {
    }
    return render(request, 'board/themes/{}/portal.html'.format(BOARD_THEME), context)
