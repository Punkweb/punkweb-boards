"""django_boards URL Configuration

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
from graphene_django.views import GraphQLView

from django_boards import settings
from django_boards import views

app_name = "django_boards"

urlpatterns = [
    # url(r'^$', views.portal_view, name='portal'),
    url(r'^board/', include('apps.board.urls')),
    url(r'^board/page/', include('apps.pages.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^captcha/', include('captcha.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
