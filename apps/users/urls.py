from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^me/$', views.my_profile, name='me'),
    url(r'^settings/$', views.settings_view, name='settings'),
    url(r'^profile/(?P<user_id>[^/]+)/$', views.profile_view, name='profile'),
]
