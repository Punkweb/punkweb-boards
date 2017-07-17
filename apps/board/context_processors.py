from .settings import BOARD_THEME, SHOUTBOX_ENABLED
from apps.api.models import Report


def settings(request):
    return {
        'BOARD_SETTINGS': {
            'BOARD_THEME': BOARD_THEME,
            'SHOUTBOX_ENABLED': SHOUTBOX_ENABLED
        }
    }


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
            'unread_notifications':
                request.user.notifications.filter(read=False).count()
        })
        if request.user.is_staff:
            unresolved_reports = Report.objects.filter(resolved=False).count()
            ctx.update({'unresolved_reports': unresolved_reports})
    return ctx
