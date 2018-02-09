from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django_boards.models import (Category, Subcategory, Thread, Post, Conversation, Message,
    Report, Shout)
from django_boards.rest.serializers import (CategorySerializer, SubcategorySerializer,
    ThreadSerializer, PostSerializer, MessageSerializer, ShoutSerializer,
    ConversationSerializer, UserSerializer)
from django_boards.rest.permissions import IsTargetUser, BelongsToUser
from django_boards import queries


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = get_user_model().objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsTargetUser,)

    @list_route()
    def from_token(self, request, *args, **kwargs):
        token_string = request.query_params.get('token')
        if not token_string:
            return Response('Token query param required', status=400)
        token = get_object_or_404(Token, key=token_string)
        self.kwargs['pk'] = token.user_id
        user = self.get_object()
        return Response(self.get_serializer(user).data)


class ObtainAuthToken(OriginalObtain):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })
obtain_auth_token = ObtainAuthToken.as_view()


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.order_by('order')
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
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
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Subcategory.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False, parent__auth_req=False)
        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            qs = qs.filter(parent__id=parent_id)
        return qs.all()


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Thread.objects.order_by('-created')
    serializer_class = ThreadSerializer
    permission_classes = (BelongsToUser,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Thread.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                category__auth_req=False,
                category__parent__auth_req=False)
        subcategory_id = self.request.query_params.get('subcategory_id')
        if subcategory_id:
            qs = qs.filter(category__id=subcategory_id)
        return qs.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Thread.objects.none()
        serializer.save(user=self.request.user)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer
    permission_classes = (BelongsToUser,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Post.objects.none()
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                thread__category__auth_req=False,
                thread__category__parent__auth_req=False)
        return qs.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Post.objects.none()
        serializer.save(user=self.request.user)


class ConversationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Conversation.objects.none()
        qs = self.queryset
        qs = qs.filter(users__in=[self.request.user])
        return qs.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Conversation.objects.none()
        serializer.save(user=self.request.user)


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Message.objects.none()
        qs = self.queryset
        qs = qs.filter(conversation__users__in=[self.request.user])
        return qs.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Message.objects.none()
        serializer.save(user=self.request.user)


class ShoutViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Shout.objects.all()[:25]
    serializer_class = ShoutSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.profile.is_banned:
            return Shout.objects.none()
        serializer.save(user=self.request.user)


class StatisticsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        total_posts = Post.objects.count()
        total_threads = Thread.objects.count()
        total_members = get_user_model().objects.count()
        posts_by_dow = queries.posts_by_dow()
        threads_by_dow = queries.threads_by_dow()
        threads_in_subcategories = queries.threads_in_subcategories()
        return Response({
            'total_posts': total_posts,
            'total_threads': total_threads,
            'total_members': total_members,
            'posts_by_dow': posts_by_dow,
            'threads_by_dow': threads_by_dow,
            'threads_in_subcategories': threads_in_subcategories
        })
