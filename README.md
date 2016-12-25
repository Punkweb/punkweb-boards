# django-boards
Django forum boards with django-bbcode support.


### A note about sceditor (BBCode editor)

In order to keep this repository clean I am not including the source for the
bbcode editor in the static assets folder.


I may make a separate repository for the bbcode editor, as I plan to hack it to
fit special needs for this project.


For now, download [SCEditor](http://www.sceditor.com/) and unzip it at:
`django-boards/static-assets/sceditor/`



### Some custom bbcode tags

Check out custom_tags.txt for a list of bbcode tag definitions and replacement
html.  Add these in the admin panel.


### Almost ready for use!

Check out the 'Ready' milestone under issues to see what's left before this is at
a usable state.


Currently using Bootstrap for the layout so that I can get everything working
quickly.  This will change shortly and a custom theme layout will be added.
