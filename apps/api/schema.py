from graphene import relay, List
from graphene_django.types import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
from .models import (EmailUser, UserRank, Category, Subcategory, Thread, Post,
    Conversation, Message, Report, Shout, Notification,)


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


class Query(object):
    all_users = List(EmailUserNode)
    all_categories = List(CategoryNode)
    all_subcategories = List(SubcategoryNode)

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
            qs = qs.filter(auth_req=False)
        return qs.all()
