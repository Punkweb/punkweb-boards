from django.conf.urls import url

from punkweb_boards import views

urlpatterns = [
    url(r"^not-found/$", views.page_not_found_view, name="not-found"),
    url(r"^(?P<slug>[\w-]+)/$", views.page_view, name="page"),
]
