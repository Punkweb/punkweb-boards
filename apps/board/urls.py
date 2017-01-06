from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^', include('apps.users.urls')),
    url(r'^unpermitted/$',
        views.unpermitted_view, name='unpermitted'),

    url(r'^category/(?P<pk>[^/]+)/$',
        views.category_view, name='category'),
    url(r'^subcategory/(?P<pk>[^/]+)/$',
        views.subcategory_view, name='subcategory'),
    url(r'^thread/(?P<pk>[^/]+)/$',
        views.thread_view, name='thread'),

    url(r'^messages/$',
        views.conversations_list, name='conversations-list'),

    url(r'^create_thread/(?P<category_id>[^/]+)/$',
        views.thread_create, name='thread-create'),
    url(r'^update_thread/(?P<pk>[^/]+)/$',
        views.thread_update, name='thread-update'),
    url(r'^delete_thread/(?P<pk>[^/]+)/$',
        views.thread_delete, name='thread-delete'),

    url(r'^update_post/(?P<pk>[^/]+)/$',
        views.post_update, name='post-update'),
    url(r'^delete_post/(?P<pk>[^/]+)/$',
        views.post_delete, name='post-delete'),

    url(r'^reports/$',
        views.reports_list, name='reports-list'),
    url(r'^report/(?P<pk>[^/]+)/',
        views.report_view, name='report'),
    url(r'^report_thread/(?P<thread>[^/]+)/$',
        views.report_create, name='report-thread'),
    url(r'^report_post/(?P<post>[^/]+)/$',
        views.report_create, name='report-post'),
]
