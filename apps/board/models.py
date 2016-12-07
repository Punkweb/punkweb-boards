from django.db import models
from precise_bbcode.fields import BBCodeTextField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey
from apps.users.models import EmailUser


class ParentCategory(UUIDPrimaryKey):
    name = models.CharField(max_length=96, blank=False, null=False, unique=True)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'parent category'
        verbose_name_plural = 'parent categories'

    def __str__(self):
        return "{}. {}".format(self.order, self.name)


class ChildCategory(UUIDPrimaryKey):
    parent = models.ForeignKey(
        ParentCategory, blank=True, null=True, default=None)
    name = models.CharField(max_length=96, blank=False, null=False)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'child category'
        verbose_name_plural = 'child categories'

    def __str__(self):
        return "{}. {}".format(self.order, self.name)


class Post(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(EmailUser, blank=False, null=False)
    category = models.ForeignKey(ChildCategory, blank=False, null=False)
    title = models.CharField(max_length=96, blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return self.title


class Comment(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(EmailUser, blank=False, null=False)
    post = models.ForeignKey(Post, blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return '{}\'s comment on {} {}'.format(self.user, self.post, self.created)
