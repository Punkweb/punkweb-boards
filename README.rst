punkweb-boards
=====================

Downtime
~~~~~~~~~~~~~~~~~~~~~
Right now punkweb is experiencing some downtime as the www.punkweb.us domain
expired.  We'll be back up ASAP on www.punkweb.net!

Django forum boards with bbcode support.

This project aims to be a full featured **classic style** forum board.  As opposed to the
new *modern* style of discussion board, such as discourse.

Note: Renamed from django-boards to punkweb-boards
~~~~~~~~~~~~~~~~~~~~~

Sorry if this causes any inconvience, but I added the following management command
you can use to rename your existing tables without losing any data:

https://gist.github.com/rafaponieman/201054ddf725cda1e60be3fe845850a5

rename.sh

::

    #/bin/bash

    ./manage.py rename_tables django_boards punkweb_boards boardprofile category conversation message notification page post report shout subcategory thread userrank
    ./manage.py rename_tables django_boards punkweb_boards boardprofile_downvoted_by boardprofile_ranks boardprofile_upvoted_by conversation_unread_by conversation_users post_downvoted_by post_upvoted_by thread_upvoted_by thread_downvoted_by


run ./rename.sh and you should be good.

Demo/Documentation
~~~~~~~~~~~~~~~~~~

Check out our community at `PunkWeb <https://punkweb.net/board/>`__ for a
live demonstration of punkweb-boards, or view the
`documentation <https://punkweb.net/board/page/docs-index/>`__!

I'm just getting started on the documentation, there's dozens of pages I still
need to write out, but what's there now should help get you started.

Ready (somewhat) for use!
~~~~~~~~~~~~~~~~~~~~~

Punkweb is currently being hosted in production using Punkweb Boards for it's forum
software.  With that being said, you could very well use this in production for your
own community but only if you're willing to accept some things to not work or be
as robust as you'd like for the time being.

Now that the project is designed as a reusable app format, you could start using it
today, and be pleasantly surprised when things change.

Check out the 'Ready' milestone under issues to see what's left before I release
a solid v1.0.0.
