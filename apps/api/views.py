from rest_framework import viewsets, permissions

from apps.board.models import Category, Subcategory, Thread, Post, \
    Conversation, Message, Report, Shout
from .serializers import CategorySerializer, SubcategorySerializer, \
    ThreadSerializer, PostSerializer, MessageSerializer, ReportSerializer, \
    ShoutSerializer, ConversationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('order')
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False)
        return qs.all()


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.order_by('order')
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(auth_req=False, parent__auth_req=False)
        return qs.all()


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.order_by('-created')
    serializer_class = ThreadSerializer

    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                category__auth_req=False,
                category__parent__auth_req=False)
        return qs.all()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_authenticated:
            qs = qs.filter(
                thread__category__auth_req=False,
                thread__category__parent__auth_req=False)
        return qs.all()


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAdminUser,)


class ShoutViewSet(viewsets.ModelViewSet):
    queryset = Shout.objects.all()
    serializer_class = ShoutSerializer
