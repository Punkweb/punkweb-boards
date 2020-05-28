from django.conf.urls import url, include
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

router.register(r"board/categories", CategoryViewSet, "categories")
router.register(r"board/subcategories", SubcategoryViewSet, "subcategories")
router.register(r"board/threads", ThreadViewSet, "threads")
router.register(r"board/posts", PostViewSet, "posts")
router.register(r"board/conversations", ConversationViewSet, "conversations")
router.register(r"board/messages", MessageViewSet, "messages")
router.register(r"board/shouts", ShoutViewSet, "shouts")
router.register(r"board/profiles", BoardProfileViewSet, "profiles")
router.register(r"users", UserViewSet, "users")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^token-auth/", obtain_auth_token),
    url(r"^register/", UserCreateView.as_view(), name='create-account'),
]
