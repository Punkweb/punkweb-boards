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

router.register(r"board/categories", CategoryViewSet, base_name="categories")
router.register(r"board/subcategories", SubcategoryViewSet, base_name="subcategories")
router.register(r"board/threads", ThreadViewSet, base_name="threads")
router.register(r"board/posts", PostViewSet, base_name="posts")
router.register(r"board/conversations", ConversationViewSet, base_name="conversations")
router.register(r"board/messages", MessageViewSet, base_name="messages")
router.register(r"board/shouts", ShoutViewSet, base_name="shouts")
router.register(r"board/profiles", BoardProfileViewSet, base_name="profiles")
router.register(r"users", UserViewSet, base_name="users")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^token-auth/", obtain_auth_token),
    url(r"^register/", UserCreateView.as_view(), name='create-account'),
]
