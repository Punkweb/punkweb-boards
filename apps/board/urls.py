from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index_view, name='index'),
    url(r'^unpermitted/$', views.unpermitted_view, name='unpermitted'),

    url(r'^category/(?P<pk>[^/]+)/$', views.category_view, name='category'),
    url(r'^subcategory/(?P<pk>[^/]+)/$', views.subcategory_view, name='subcategory'),
    url(r'^thread/(?P<pk>[^/]+)/$', views.thread_view, name='thread'),
    url(r'^shoutbox/$', views.shouts_view, name='shoutbox'),

    url(r'^create_category/$',
        views.CategoryCreate.as_view(), name='category-create'),
    url(r'^update_category/(?P<pk>[^/]+)/$',
        views.CategoryUpdate.as_view(), name='category-update'),
    url(r'^delete_category/(?P<pk>[^/]+)/$',
        views.CategoryDelete.as_view(), name='category-delete'),

    url(r'^create_subcategory/(?P<category_id>[^/]+)/$',
        views.SubcategoryCreate.as_view(), name='subcategory-create'),
    url(r'^update_subcategory/(?P<pk>[^/]+)/$',
        views.SubcategoryUpdate.as_view(), name='subcategory-update'),
    url(r'^delete_subcategory/(?P<pk>[^/]+)/$',
        views.SubcategoryDelete.as_view(), name='subcategory-delete'),

    url(r'^create_thread/(?P<category_id>[^/]+)/$',
        views.ThreadCreate.as_view(), name='thread-create'),
    url(r'^update_thread/(?P<pk>[^/]+)/$',
        views.ThreadUpdate.as_view(), name='thread-update'),
    url(r'^delete_thread/(?P<pk>[^/]+)/$',
        views.ThreadDelete.as_view(), name='thread-delete'),

    url(r'^create_post/(?P<thread_id>[^/]+)/$',
        views.PostCreate.as_view(), name='post-create'),
    url(r'^update_post/(?P<pk>[^/]+)/$',
        views.PostUpdate.as_view(), name='post-update'),
    url(r'^delete_post/(?P<pk>[^/]+)/$',
        views.PostDelete.as_view(), name='post-delete'),
]
