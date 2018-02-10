from django_boards.conf import settings as BOARD_SETTINGS
from django_boards.models import Report


def settings(request):
    return {
        'BOARD_SETTINGS': {
            'BOARD_NAME': BOARD_SETTINGS.BOARD_NAME,
            'BOARD_THEME': BOARD_SETTINGS.BOARD_THEME,
            'SHOUTBOX_ENABLED': BOARD_SETTINGS.SHOUTBOX_ENABLED,
            'SIGNATURES_ENABLED': BOARD_SETTINGS.SIGNATURES_ENABLED,
            'USER_BIRTHDAY_MESSAGE': BOARD_SETTINGS.USER_BIRTHDAY_MESSAGE,
            'GLOBAL_BIRTHDAYS': BOARD_SETTINGS.GLOBAL_BIRTHDAYS,
        }
    }


def base_context(request):
    ctx = {}
    if request.user.is_authenticated and not request.user.profile.is_banned:
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
