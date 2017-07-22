from apps.board import settings as BOARD_SETTINGS
from precise_bbcode.bbcode import get_parser

def tagged_usernames(content):
    usernames = []
    if '[user]' in content.lower():
        user_tags = content.split('[user]')
        for tag in user_tags:
            if '[/user]' in tag:
                username = tag[:tag.index('[/user]')]
                usernames.append(username)
    return usernames

def render_example_username(rank, username):
    parser = get_parser()
    return parser.render(rank.username_modifier.replace('{USER}', username))

def render_username(user):
    # Returns the username rendered in bbcode defined by the users rank.
    a = BOARD_SETTINGS.USERNAME_MODIFIERS_ENABLED
    parser = get_parser()
    if user.is_banned:
        return 'BANNED'
    if a and user.username_modifier:
        modifier = user.username_modifier
        replace_username = modifier.replace('{USER}', user.username)
        return parser.render(replace_username)
    elif a and user.rank and user.rank.username_modifier:
        modifier = user.rank.username_modifier
        replace_username = modifier.replace('{USER}', user.username)
        return parser.render(replace_username)
    else:
        return user.username
