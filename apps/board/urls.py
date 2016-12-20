from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^category/(?P<pk>[^/]+)/$', views.category_view, name='category'),
    url(r'^subcategory/(?P<pk>[^/]+)/$', views.subcategory_view, name='subcategory'),
    url(r'^shoutbox/$', views.shouts_view, name='shoutbox'),

    url(r'^post/(?P<pk>[^/]+)/$', views.post_view, name='post'),
    url(r'^create_post/(?P<category_id>[^/]+)/$', views.PostCreate.as_view(), name='post-create'),
    url(r'^update_post/(?P<pk>[^/]+)/$', views.PostUpdate.as_view(), name='post-update'),
    url(r'^delete_post/(?P<pk>[^/]+)/$', views.PostDelete.as_view(), name='post-delete'),

    url(r'^create_comment/(?P<post_id>[^/]+)/$', views.CommentCreate.as_view(), name='comment-create'),
    url(r'^update_comment/(?P<pk>[^/]+)/$', views.CommentUpdate.as_view(), name='comment-update'),
    url(r'^delete_comment/(?P<pk>[^/]+)/$', views.CommentDelete.as_view(), name='comment-delete'),

    url(r'^create_category/$', views.CategoryCreate.as_view(), name='category-create'),
    url(r'^update_category/(?P<pk>[^/]+)/$', views.CategoryUpdate.as_view(), name='category-update'),
    url(r'^delete_category/(?P<pk>[^/]+)/$', views.CategoryDelete.as_view(), name='category-delete'),

    url(r'^create_subcategory/(?P<category_id>[^/]+)/$', views.SubcategoryCreate.as_view(), name='subcategory-create'),
    url(r'^update_subcategory/(?P<pk>[^/]+)/$', views.SubcategoryUpdate.as_view(), name='subcategory-update'),
    url(r'^delete_subcategory/(?P<pk>[^/]+)/$', views.SubcategoryDelete.as_view(), name='subcategory-delete'),

    url(r'^create_comment/(?P<post_id>[^/]+)/$', views.CommentCreate.as_view(), name='comment-create'),
    url(r'^update_comment/(?P<pk>[^/]+)/$', views.CommentUpdate.as_view(), name='comment-update'),
    url(r'^delete_comment/(?P<pk>[^/]+)/$', views.CommentDelete.as_view(), name='comment-delete'),
]
