from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^conversations/$',
        views.conversations_list, name='list'),
    url(r'^update_conversation/(?P<pk>[^/]+)/$',
        views.ConversationUpdate.as_view(), name='conversation-update'),

    url(r'^create_message/$',
        views.MessageCreate.as_view(), name='message-create'),
    url(r'^update_message/(?P<pk>[^/]+)/$',
        views.MessageUpdate.as_view(), name='message-update'),
    url(r'^delete_message/(?P<pk>[^/]+)/$',
        views.MessageDelete.as_view(), name='message-delete'),
]
