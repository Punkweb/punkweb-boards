import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework.authtoken.models import Token
from punkweb_boards.conf import settings as BOARD_SETTINGS


def get_actual_user(request):
    if request.user is None:
        return None

    return request.user


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_actual_user(request))
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            name = request.user.username.replace(" ", "_")
            cache.set(
                "seen_%s" % (name), now, BOARD_SETTINGS.USER_LASTSEEN_TIMEOUT
            )
