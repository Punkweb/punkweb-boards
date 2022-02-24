from django.urls import include, path
from rest_framework import routers

from punkweb_boards.rest.views import (
    BoardProfileViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ThreadViewSet,
    PostViewSet,
    ConversationViewSet,
    MessageViewSet,
    ShoutViewSet,
)

router = routers.DefaultRouter()

router.register(r"board/categories", CategoryViewSet, basename="categories")
router.register(r"board/subcategories", SubcategoryViewSet, basename="subcategories")
router.register(r"board/threads", ThreadViewSet, basename="threads")
router.register(r"board/posts", PostViewSet, basename="posts")
router.register(r"board/conversations", ConversationViewSet, basename="conversations")
router.register(r"board/messages", MessageViewSet, basename="messages")
router.register(r"board/shouts", ShoutViewSet, basename="shouts")
router.register(r"board/profiles", BoardProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
]
