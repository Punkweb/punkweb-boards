# django-boards - punkweb
Django forum boards with django-bbcode support.

## Quick start

### Installation and running
`pip install -r requirements.txt

./db.sh

./manage.py makemigrations

./manage.py migrate

./manage.py runserver`

### Create a super user
`
./manage.py createsuperuser
`

### Customize forum

Navigate to `0.0.0.0/admin/`, login and start by adding categories, bbcode tags, emoticons, and music.

Switch themes at
`/django-boards/apps/board/settings.py`


### A note about sceditor (BBCode editor)

In order to keep this repository clean I am not including the source for the
bbcode editor in the static assets folder.


I may make a separate repository for the bbcode editor, as I plan to hack it to
fit special needs for this project.


For now, download [SCEditor](http://www.sceditor.com/) and unzip it at:
`django-boards/static/sceditor/`



### Some custom bbcode tags

Check out custom_tags.txt for a list of bbcode tag definitions and replacement
html.  Add these in the admin page.


### Features

Check out features.txt for a list of current and upcoming features.


### Almost ready for use!

Check out the 'Ready' milestone under issues to see what's left before this is at
a usable state.


Currently using Bootstrap for the layout so that I can get everything working
quickly.  This will change shortly and a custom theme layout will be added.
