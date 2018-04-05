from django.conf.urls import url
import django.contrib.auth.views as auth_views

from punkweb_boards.conf.settings import BOARD_THEME
from punkweb_boards import views

app_name = 'board'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^unpermitted/$', views.unpermitted_view, name='unpermitted'),
    url(r'^register/$', views.registration_view, name='register'),
    url(
        r'^login/$',
        auth_views.login,
        {
            'template_name': 'punkweb_boards/themes/{}/login.html'.format(
                BOARD_THEME
            )
        },
        name='login',
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/board/login/'},
        name='logout',
    ),
    url(r'^me/$', views.my_profile, name='me'),
    url(r'^settings/$', views.settings_view, name='settings'),
    url(r'^profile/(?P<username>[^/]+)/$', views.profile_view, name='profile'),
    url(r'^search/$', views.keyword_search_view, name='search'),
    url(r'^category/(?P<pk>[^/]+)/$', views.category_detail, name='category-detail'),
    url(
        r'^create_category/$',
        views.category_create,
        name='category-create',
    ),
    url(
        r'^update_category/(?P<pk>[^/]+)/$',
        views.category_update,
        name='category-update',
    ),
    url(
        r'^delete_category/(?P<pk>[^/]+)/$',
        views.category_delete,
        name='category-delete',
    ),
    url(
        r'^subcategory/(?P<pk>[^/]+)/$',
        views.subcategory_detail,
        name='subcategory-detail',
    ),
    url(
        r'^create_category/$',
        views.category_create,
        name='category-create',
    ),
    url(
        r'^update_category/(?P<pk>[^/]+)/$',
        views.category_update,
        name='category-update',
    ),
    url(
        r'^delete_category/(?P<pk>[^/]+)/$',
        views.category_delete,
        name='category-delete',
    ),
    url(r'^inbox/$', views.conversation_list, name='conversation-list'),
    url(
        r'^conversation/(?P<pk>[^/]+)/$',
        views.conversation_detail,
        name='conversation',
    ),
    url(
        r'^create_conversation',
        views.conversation_create,
        name='conversation-create',
    ),
    url(
        r'^update_message/(?P<pk>[^/]+)/$',
        views.message_update,
        name='message-update',
    ),
    url(
        r'^delete_message/(?P<pk>[^/]+)/$',
        views.message_delete,
        name='message-delete',
    ),
    url(r'^thread/(?P<pk>[^/]+)/?$', views.thread_view, name='thread'),
    url(
        r'^create_thread/(?P<category_id>[^/]+)/$',
        views.thread_create,
        name='thread-create',
    ),
    url(
        r'^update_thread/(?P<pk>[^/]+)/$',
        views.thread_update,
        name='thread-update',
    ),
    url(
        r'^delete_thread/(?P<pk>[^/]+)/$',
        views.thread_delete,
        name='thread-delete',
    ),
    url(
        r'^update_post/(?P<pk>[^/]+)/$', views.post_update, name='post-update'
    ),
    url(
        r'^delete_post/(?P<pk>[^/]+)/$', views.post_delete, name='post-delete'
    ),
    url(r'^reports/$', views.reports_list, name='reports-list'),
    url(r'^report/(?P<pk>[^/]+)/', views.report_view, name='report'),
    url(
        r'^report_thread/(?P<thread>[^/]+)/$',
        views.report_create,
        name='report-thread',
    ),
    url(
        r'^report_post/(?P<post>[^/]+)/$',
        views.report_create,
        name='report-post',
    ),
    url(r'^members/$', views.members_list, name='members-list'),
    url(r'^statistics/$', views.statistics_view, name='statistics'),
    url(
        r'^notification_redirect/(?P<pk>[^/]+)/$',
        views.notification_redirect,
        name='notification-redirect',
    ),
]
