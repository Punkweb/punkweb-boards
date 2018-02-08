from django.conf.urls import url

from django_boards import views

app_name = 'pages'

urlpatterns = [
    url(r'^not-found/$', views.page_not_found_view, name='not-found'),
    url(r'^(?P<slug>[\w-]+)/$', views.page_view, name='page'),
]
