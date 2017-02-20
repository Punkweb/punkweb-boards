from rest_framework import viewsets

from apps.board.models import Category, Subcategory, Thread, Post, \
    Conversation, Message, Report, Shout
from .serializers import CategorySerializer, SubcategorySerializer, \
    ThreadSerializer, PostSerializer, MessageSerializer, ReportSerializer, \
    ShoutSerializer, ConversationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('order')
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.order_by('order')
    serializer_class = SubcategorySerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.order_by('-created')
    serializer_class = ThreadSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ShoutViewSet(viewsets.ModelViewSet):
    queryset = Shout.objects.all()
    serializer_class = ShoutSerializer
