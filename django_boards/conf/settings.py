from django.conf import settings

SETTINGS_OVERRIDES = getattr(settings, 'DJANGO_BOARDS', {})

BOARD_NAME = SETTINGS_OVERRIDES.get('BOARD_NAME', 'Django Boards')

# Theme (punkweb)
BOARD_THEME = SETTINGS_OVERRIDES.get('BOARD_THEME', 'punkweb')

# Display user signatures and allow users to set them in profile settings
SIGNATURES_ENABLED = SETTINGS_OVERRIDES.get('SIGNATURES_ENABLED', True)

USERNAME_MODIFIERS_ENABLED = SETTINGS_OVERRIDES.get('USERNAME_MODIFIERS_ENABLED', True)

# Happy birthday message only the user can see
USER_BIRTHDAY_MESSAGE = SETTINGS_OVERRIDES.get('USER_BIRTHDAY_MESSAGE', True)

# Shoutbox settings
SHOUTBOX_ENABLED = SETTINGS_OVERRIDES.get('SHOUTBOX_ENABLED', True)
SHOUTBOX_MINIMUM_POSTS = SETTINGS_OVERRIDES.get('SHOUTBOX_MINIMUM_POSTS', False)
SHOUTBOX_MINIMUM_POSTS_REQ = SETTINGS_OVERRIDES.get('SHOUTBOX_MINIMUM_POSTS_REQ', 25)
SHOUTBOX_DISABLED_TAGS = SETTINGS_OVERRIDES.get('SHOUTBOX_DISABLED_TAGS', [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube', 'code',
])

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = SETTINGS_OVERRIDES.get('USER_ONLINE_TIMEOUT', 300)

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = SETTINGS_OVERRIDES.get('USER_LASTSEEN_TIMEOUT', 60 * 60 * 24 * 7)

# Require captcha on registration
CAPTCHAS_ENABLED = SETTINGS_OVERRIDES.get('CAPTCHAS_ENABLED', False)

# TODO: FUTURE -----------------------------------------------------------------

GLOBAL_BIRTHDAYS = SETTINGS_OVERRIDES.get('GLOBAL_BIRTHDAYS', True)

PRIVATE_MESSAGING_ENABLED = SETTINGS_OVERRIDES.get('PRIVATE_MESSAGING_ENABLED', True)

GRAVATAR_SUPPORT_ENABLED = SETTINGS_OVERRIDES.get('GRAVATAR_SUPPORT_ENABLED', True)

USERNAME_MODIFIERS_DISABLED_TAGS = SETTINGS_OVERRIDES.get('USERNAME_MODIFIERS_DISABLED_TAGS', [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube'
])

API_ENABLED = True
