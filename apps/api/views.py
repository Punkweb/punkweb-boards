from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response

from .models import (Category, Subcategory, Thread, Post, Conversation, Message,
    Report, Shout)
from .serializers import (CategorySerializer, SubcategorySerializer,
    ThreadSerializer, PostSerializer, MessageSerializer, ShoutSerializer,
    ConversationSerializer, UserSerializer)
from .permissions import IsTargetUser


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = get_user_model().objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsTargetUser,)


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.order_by('order')
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Category.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False)
        return qs.all()


class SubcategoryViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Subcategory.objects.order_by('order')
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Subcategory.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False, parent__auth_req=False)
        return qs.all()


class ThreadViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Thread.objects.order_by('-created')
    serializer_class = ThreadSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Thread.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                category__auth_req=False,
                category__parent__auth_req=False)
        return qs.all()


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Post.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                thread__category__auth_req=False,
                thread__category__parent__auth_req=False)
        return qs.all()


class ConversationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Conversation.objects.none()
        qs = self.queryset
        qs = qs.filter(users__in=[self.request.user])
        return qs.all()


class MessageViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Message.objects.none()
        qs = self.queryset
        qs = qs.filter(conversation__users__in=[self.request.user])
        return qs.all()


class ShoutViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Shout.objects.all()[:25]
    serializer_class = ShoutSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Shout.objects.none()
        serializer.save(user=self.request.user)
