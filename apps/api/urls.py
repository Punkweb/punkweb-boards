from django.conf.urls import url, include
from rest_framework import routers
from .views import (CategoryViewSet, SubcategoryViewSet, ThreadViewSet,
    PostViewSet, ConversationViewSet, MessageViewSet, ShoutViewSet, UserViewSet)

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
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
