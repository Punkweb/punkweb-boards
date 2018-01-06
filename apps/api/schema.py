from graphene import List
from graphene_django.types import DjangoObjectType
from .models import (EmailUser, Category, Subcategory, Thread, Post,
    Conversation, Message, Shout,)


class EmailUserNode(DjangoObjectType):
    class Meta:
        model = EmailUser
        exclude_fields = ('password', 'groups', 'user_permissions',)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        exclude_fields = ('auth_req',)


class SubcategoryNode(DjangoObjectType):
    class Meta:
        model = Subcategory
        exclude_fields = ('auth_req',)


class ThreadNode(DjangoObjectType):
    # TODO: Subcategory filter
    class Meta:
        model = Thread


class PostNode(DjangoObjectType):
    # TODO: Thread filter
    class Meta:
        model = Post


class ConversationNode(DjangoObjectType):
    # TODO: Must be authenticated
    class Meta:
        model = Conversation


class MessageNode(DjangoObjectType):
    # TODO: Must be authenticated
    class Meta:
        model = Message


class ShoutNode(DjangoObjectType):
    class Meta:
        model = Shout


class Query(object):
    all_users = List(EmailUserNode)
    all_categories = List(CategoryNode)
    all_subcategories = List(SubcategoryNode)
    all_threads = List(ThreadNode)
    all_posts = List(PostNode)
    all_conversations = List(ConversationNode)
    all_messsages = List(MessageNode)
    all_shouts = List(ShoutNode)

    def resolve_all_users(self, info, **kwargs):
        qs = EmailUser.objects.order_by('username')
        return qs.all()

    def resolve_all_categories(self, info, **kwargs):
        qs = Category.objects.order_by('order')
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Category.objects.none()
        if not user.is_authenticated():
            qs = qs.filter(auth_req=False)
        return qs.all()

    def resolve_all_subcategories(self, info, **kwargs):
        qs = Subcategory.objects.order_by('order')
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Subcategory.objects.none()
        if not user.is_authenticated():
            qs = qs.filter(auth_req=False, parent__auth_req=False)
        return qs.all()

    def resolve_all_threads(self, info, **kwargs):
        qs = Thread.objects.order_by('-created')
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Thread.objects.none()
        if not user.is_authenticated():
            qs = qs.filter(
                category__auth_req=False,
                category__parent__auth_req=False)
        return qs.all()

    def resolve_all_posts(self, info, **kwargs):
        qs = Post.objects.order_by('-created')
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Post.objects.none()
        if not user.is_authenticated():
            qs = qs.filter(
                thread__category__auth_req=False,
                thread__category__parent__auth_req=False)
        return qs.all()

    def resolve_all_conversations(self, info, **kwargs):
        qs = Conversation.objects.all()
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Conversation.objects.none()
        qs = qs.filter(users__in=[user])
        return qs.all()

    def resolve_all_messages(self, info, **kwargs):
        qs = Message.objects.all()
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Message.objects.none()
        qs = qs.filter(conversation__users__in=[user])
        return qs.all()

    def resolve_all_shouts(self, info, **kwargs):
        qs = Shout.objects.all()[:25]
        user = info.context.user

        if user.is_authenticated() and user.is_banned:
            return Shout.objects.none()
        return qs.all()
