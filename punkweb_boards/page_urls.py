from django.urls import re_path

from punkweb_boards import views

urlpatterns = [
    re_path(r"^not-found/$", views.page_not_found_view, name="not-found"),
    re_path(r"^(?P<slug>[\w-]+)/$", views.page_view, name="page"),
]
