from rest_framework import viewsets
from .models import ParentCategory, ChildCategory, Post, Comment
from .serializers import ParentCategorySerializer, ChildCategorySerializer, \
    PostSerializer, CommentSerializer


class ParentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ParentCategory.objects.all().order_by('order')
    serializer_class = ParentCategorySerializer


class ChildCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChildCategory.objects.all().order_by('order')
    serializer_class = ChildCategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
