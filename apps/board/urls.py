from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^category/(?P<category_id>[^/]+)/$', views.category_view, name='category'),
    url(r'^topic/(?P<category_id>[^/]+)/$', views.topic_view, name='topic'),
    url(r'^post/(?P<post_id>[^/]+)/$', views.post_view, name='post'),
    url(r'^shoutbox/$', views.shouts_view, name='shoutbox')
]
