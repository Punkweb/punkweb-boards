from django.urls import include, re_path
import django.contrib.auth.views as auth_views

from punkweb_boards.conf.settings import BOARD_THEME
from punkweb_boards import views

app_name = "board"

urlpatterns = [
    re_path(r"^$", views.index_view, name="index"),
    re_path(r"^page/", include("punkweb_boards.page_urls")),
    re_path(r"^unpermitted/$", views.unpermitted_view, name="unpermitted"),
    re_path(r"^register/$", views.registration_view, name="register"),
    re_path(
        r"^login/$",
        auth_views.LoginView.as_view(
            template_name="punkweb_boards/themes/{}/login.html".format(BOARD_THEME)
        ),
        name="login",
    ),
    re_path(
        r"^logout/$",
        auth_views.LogoutView.as_view(),
        {"next_page": "/board/login/"},
        name="logout",
    ),
    re_path(r"^me/$", views.my_profile, name="me"),
    re_path(r"^settings/$", views.settings_view, name="settings"),
    re_path(r"^profile/(?P<username>[^/]+)/$", views.profile_view, name="profile"),
    re_path(r"^search/$", views.keyword_search_view, name="search"),
    re_path(
        r"^category/(?P<pk>[^/]+)/$",
        views.category_detail,
        name="category-detail",
    ),
    re_path(r"^create_category/$", views.category_create, name="category-create"),
    re_path(
        r"^update_category/(?P<pk>[^/]+)/$",
        views.category_update,
        name="category-update",
    ),
    re_path(
        r"^delete_category/(?P<pk>[^/]+)/$",
        views.category_delete,
        name="category-delete",
    ),
    re_path(
        r"^subcategory/(?P<pk>[^/]+)/$",
        views.subcategory_detail,
        name="subcategory-detail",
    ),
    re_path(r"^create_category/$", views.category_create, name="category-create"),
    re_path(
        r"^update_category/(?P<pk>[^/]+)/$",
        views.category_update,
        name="category-update",
    ),
    re_path(
        r"^delete_category/(?P<pk>[^/]+)/$",
        views.category_delete,
        name="category-delete",
    ),
    re_path(r"^thread/(?P<pk>[^/]+)/?$", views.thread_view, name="thread"),
    re_path(
        r"^create_thread/(?P<category_id>[^/]+)/$",
        views.thread_create,
        name="thread-create",
    ),
    re_path(
        r"^update_thread/(?P<pk>[^/]+)/$",
        views.thread_update,
        name="thread-update",
    ),
    re_path(
        r"^delete_thread/(?P<pk>[^/]+)/$",
        views.thread_delete,
        name="thread-delete",
    ),
    re_path(r"^update_post/(?P<pk>[^/]+)/$", views.post_update, name="post-update"),
    re_path(r"^delete_post/(?P<pk>[^/]+)/$", views.post_delete, name="post-delete"),
    re_path(r"^reports/$", views.reports_list, name="reports-list"),
    re_path(r"^report/(?P<pk>[^/]+)/", views.report_view, name="report"),
    re_path(
        r"^report_thread/(?P<thread>[^/]+)/$",
        views.report_create,
        name="report-thread",
    ),
    re_path(
        r"^report_post/(?P<post>[^/]+)/$",
        views.report_create,
        name="report-post",
    ),
    re_path(r"^members/$", views.members_list, name="members-list"),
    re_path(
        r"^notification_redirect/(?P<pk>[^/]+)/$",
        views.notification_redirect,
        name="notification-redirect",
    ),
]
