from django.conf.urls import url

from apps.pages import views

app_name = 'pages'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.page_view, name='page'),
]
