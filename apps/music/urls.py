from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^audio/(?P<slug>[\w-]+)/$', views.audio_view, name='audio'),
]
