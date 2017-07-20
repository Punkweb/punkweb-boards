# Happy birthday message only the user can see
USER_BIRTHDAY_MESSAGE = True
# Show a list of users with birthdays today
GLOBAL_BIRTHDAYS = True # TODO: create component for this
# Display user signatures and allow users to set them in profile settings
SIGNATURES_ENABLED = True

# Theme (bootstrap3, punkweb)
BOARD_THEME = 'punkweb'

# Shoutbox settings
SHOUTBOX_ENABLED = True
SHOUTBOX_MINIMUM_POSTS = False
SHOUTBOX_MINIMUM_POSTS_REQ = 25
SHOUTBOX_DEFAULT_CLOSED = True
SHOUTBOX_DISABLED_TAGS = [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube'
]

USERNAME_MODIFIERS_ENABLED = True
# TODO: Make disabled tags work
USERNAME_MODIFIERS_DISABLED_TAGS = [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube'
]
