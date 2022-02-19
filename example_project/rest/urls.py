from django.urls import include, re_path
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

from example_project.rest.views import (
    UserViewSet,
    UserCreateView,
    obtain_auth_token,
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
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^token-auth/", obtain_auth_token),
    re_path(r"^register/", UserCreateView.as_view(), name="create-account"),
]
