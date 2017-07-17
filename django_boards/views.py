from django.shortcuts import render

from apps.board.settings import BOARD_THEME

from apps.api.models import Thread

def portal_view(request):
    recent_threads = Thread.objects.all().order_by('-created')
    recent_activity = Thread.objects.all().order_by('-modified')
    if not request.user.is_authenticated:
        # Filter out activity in subcategories with auth_req = True
        recent_threads = recent_threads.filter(
            category__auth_req=False)
        recent_activity = recent_activity.filter(
            category__auth_req=False)

    context = {
        'recent_threads': recent_threads[:5],
        'recent_activity': recent_activity[:5]
    }
    return render(request, 'board/themes/{}/portal.html'.format(BOARD_THEME), context)
