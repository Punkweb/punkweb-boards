"""
URL configuration for example_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
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
    path("admin/", admin.site.urls),
    path("board/", include("punkweb_boards.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
