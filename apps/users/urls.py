from django.conf.urls import url
import django.contrib.auth.views as auth_views

from . import views

urlpatterns = [
    url(r'^register', views.register_view, name='register'),
    url(r'^login/$',
        auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$',
        auth_views.logout, {'next_page': '/users/login/'}, name='logout'),
    url(r'^me/$', views.my_profile, name='me'),
    url(r'^settings/$', views.settings_view, name='settings'),
    url(r'^profile/(?P<username>[^/]+)/$', views.profile_view, name='profile'),
]
