from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^audio/(?P<slug>[\w-]+)/$', views.audio_view, name='audio'),
    url(r'^audio/compilation/(?P<slug>[\w-]+)/$',
        views.audio_compilation_view, name='audio_compilation'),
]
