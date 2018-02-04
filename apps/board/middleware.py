import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from apps.board import settings as BOARD_SETTINGS

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            name = current_user.username.replace(' ', '_')
            cache.set('seen_%s' % (name), now, BOARD_SETTINGS.USER_LASTSEEN_TIMEOUT)
