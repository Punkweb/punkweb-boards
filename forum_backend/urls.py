"""forum_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from forum_backend import settings
from forum_backend.views import HomePage, ParentCategoryPage, ChildCategoryPage, \
    PostPage, MyProfilePage, ProfilePage, ProfileSettingsPage, ShoutboxPage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^shoutbox/$', ShoutboxPage.as_view(), name='shoutbox'),
    url(r'^me/$', MyProfilePage.as_view(), name='me'),
    url(r'^profile_settings/$', ProfileSettingsPage.as_view(), name='profile_settings'),
    url(r'^profile/(?P<uuid>[^/]+)/$', ProfilePage.as_view(), name='profile'),
    url(r'^post/(?P<uuid>[^/]+)/$', PostPage.as_view(), name='post'),
    url(r'^parent_category/(?P<uuid>[^/]+)/$',
        ParentCategoryPage.as_view(), name='parent_category'),
    url(r'^child_category/(?P<uuid>[^/]+)/$',
        ChildCategoryPage.as_view(), name='child_category'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
