from django.conf.urls import url, include
from rest_framework import routers
from django_boards.rest.views import (CategoryViewSet, SubcategoryViewSet, ThreadViewSet,
    PostViewSet, ConversationViewSet, MessageViewSet, ShoutViewSet, UserViewSet,
    StatisticsView, obtain_auth_token)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'threads', ThreadViewSet)
router.register(r'posts', PostViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'shouts', ShoutViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^statistics/', StatisticsView.as_view(), name='statistics'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', obtain_auth_token),
]
