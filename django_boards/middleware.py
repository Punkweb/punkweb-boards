import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django_boards.conf import settings as BOARD_SETTINGS


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            name = request.user.username.replace(' ', '_')
            cache.set('seen_%s' % (name), now, BOARD_SETTINGS.USER_LASTSEEN_TIMEOUT)
