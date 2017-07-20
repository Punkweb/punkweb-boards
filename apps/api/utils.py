def tagged_usernames(content):
    usernames = []
    if '[user]' in content.lower():
        user_tags = content.split('[user]')
        for tag in user_tags:
            if '[/user]' in tag:
                username = tag[:tag.index('[/user]')]
                usernames.append(username)
    return usernames
