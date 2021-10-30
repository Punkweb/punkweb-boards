import datetime
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, views
from rest_framework.decorators import action
from rest_framework.response import Response

from punkweb_boards.models import (
    BoardProfile,
    Category,
    Subcategory,
    Thread,
    Post,
    Conversation,
    Message,
    Shout,
)
from punkweb_boards.rest.serializers import (
    BoardProfileSerializer,
    CategorySerializer,
    SubcategorySerializer,
    ThreadSerializer,
    PostSerializer,
    ConversationSerializer,
    MessageSerializer,
    ShoutSerializer,
)
from punkweb_boards.rest.permissions import IsTargetUser, BelongsToUser
from punkweb_boards import queries


class BoardProfileViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = BoardProfile.objects.all()
    serializer_class = BoardProfileSerializer

    def get_queryset(self):
        qs = self.queryset
        return qs.all()

    @action(detail=False, methods=["get"])
    def online(self, request, *args, **kwargs):
        qs = self.get_queryset()
        profiles = qs.all()
        online = [profile for profile in profiles if profile.online()]
        serializer = self.get_serializer(online, many=True)
        return Response(serializer.data, status=200)


class CategoryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.order_by("order")
    serializer_class = CategorySerializer

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Category.objects.none()

        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False)
        return qs.all()


class SubcategoryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Subcategory.objects.order_by("order")
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Subcategory.objects.none()

        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False, parent__auth_req=False)
        parent_id = self.request.query_params.get("parent_id")
        if parent_id:
            qs = qs.filter(parent__id=parent_id)
        return qs.all()


class ThreadViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Thread.objects.order_by("-created")
    serializer_class = ThreadSerializer
    permission_classes = (BelongsToUser,)

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Thread.objects.none()

        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                category__auth_req=False, category__parent__auth_req=False
            )
        subcategory_id = self.request.query_params.get("subcategory_id")
        if subcategory_id:
            qs = qs.filter(category__id=subcategory_id)
        return qs.all()

    @action(detail=False, methods=["get"])
    def recent_threads(self, request, *args, **kwargs):
        recent_threads = self.get_queryset().all().order_by("-created")
        return Response(
            self.get_serializer(recent_threads[:5], many=True).data
        )

    def perform_create(self, serializer):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Thread.objects.none()

        serializer.save(user=self.request.user)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.order_by("-created")
    serializer_class = PostSerializer
    permission_classes = (BelongsToUser,)

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Post.objects.none()

        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                thread__category__auth_req=False,
                thread__category__parent__auth_req=False,
            )
        return qs.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_banned:
            return Post.objects.none()

        serializer.save(user=self.request.user)


class ConversationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    There is no way to access other users conversations through here.  Only the \
    requesting user's conversations are returned.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Conversation.objects.none()

        qs = self.queryset
        qs = qs.filter(users__in=[self.request.user])
        return qs.all()

    def perform_create(self, serializer):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Conversation.objects.none()

        serializer.save(user=self.request.user)


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Message.objects.none()

        qs = self.queryset
        qs = qs.filter(conversation__users__in=[self.request.user])
        return qs.all()

    def perform_create(self, serializer):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Message.objects.none()

        serializer.save(user=self.request.user)


class ShoutViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Shout.objects.all()
    serializer_class = ShoutSerializer

    def get_queryset(self):
        qs = self.queryset
        today = datetime.datetime.now()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        qs = qs.filter(created__range=(yesterday, today))[:25]
        return qs.all()

    def perform_create(self, serializer):
        if (
            self.request.user.is_authenticated
            and self.request.user.profile.is_banned
        ):
            return Shout.objects.none()

        serializer.save(user=self.request.user)


class StatisticsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        total_posts = Post.objects.count()
        total_threads = Thread.objects.count()
        total_members = get_user_model().objects.count()
        new_posts_this_week = queries.new_posts_this_week()
        new_threads_this_week = queries.new_threads_this_week()
        threads_in_subcategories = queries.threads_in_subcategories()
        new_members_this_week = queries.new_members_this_week()
        return Response(
            {
                "total_posts": total_posts,
                "total_threads": total_threads,
                "total_members": total_members,
                "new_posts_this_week": new_posts_this_week,
                "new_threads_this_week": new_threads_this_week,
                "new_members_this_week": new_members_this_week,
                "threads_in_subcategories": threads_in_subcategories,
            }
        )
