from django.utils.safestring import mark_safe
from precise_bbcode.bbcode import get_parser
from apps.board import settings as BOARD_SETTINGS

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
    return mark_safe(
        parser.render(rank.username_modifier.replace('{USER}', username)))

def render_username(user):
    # Returns the username rendered in bbcode defined by the users rank.
    a = BOARD_SETTINGS.USERNAME_MODIFIERS_ENABLED
    parser = get_parser()
    if user.is_banned:
        return 'BANNED'
    if a and user.username_modifier:
        modifier = user.username_modifier
        replace_username = modifier.replace('{USER}', user.username)
        return mark_safe(parser.render(replace_username))
    elif a and user.rank and user.rank.username_modifier:
        modifier = user.rank.username_modifier
        replace_username = modifier.replace('{USER}', user.username)
        return mark_safe(parser.render(replace_username))
    else:
        return user.username

def get_gravatar_url(email, size=80, secure=True, default='mm'):
    if secure:
        url_base = 'https://secure.gravatar.com/'
    else:
        url_base = 'http://www.gravatar.com/'
    email_hash = hashlib.md5(email.encode('utf-8').strip().lower()).hexdigest()
    qs = urlencode({
        's': str(size),
        'd': default,
        'r': 'pg',
    })
    url = '{}avatar/{}.jpg?{}'.format(url_base, email_hash, qs)
    return url

def has_gravatar(email):
    url = get_gravatar_url(email, default='404')
    try:
        request = Request(url)
        request.get_method = lambda: 'HEAD'
        return 200 == urlopen(request).code
    except (HTTPError, URLError):
        return False

def get_placeholder_url():
    url = '/'.join(['placeholder_profile.png'])
    # url = '{}placeholder_profile.png'.format(settings.MEDIA_ROOT)
    return url
