from django.db import models
from django.urls import reverse
from precise_bbcode.fields import BBCodeTextField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey
from apps.users.models import EmailUser


class Category(UUIDPrimaryKey):
    name = models.CharField(max_length=96, blank=False, null=False, unique=True)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return "{}. {}".format(self.order, self.name)


class Subcategory(UUIDPrimaryKey):
    parent = models.ForeignKey(
        Category, blank=True, null=True, default=None)
    name = models.CharField(max_length=96, blank=False, null=False)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return "{}. {}".format(self.order, self.name)


class Post(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(EmailUser, related_name='posts', blank=False, null=False)
    category = models.ForeignKey(Subcategory, blank=False, null=False)
    title = models.CharField(max_length=96, blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:post', kwargs={'pk': self.id})


class Comment(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(EmailUser, related_name='comments', blank=False, null=False)
    post = models.ForeignKey(Post, related_name='comments', blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return '{}\'s comment on {} {}'.format(self.user, self.post, self.created)

    def get_absolute_url(self):
        return reverse('board:post', kwargs={'pk': self.post.id})


class Shout(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(EmailUser, blank=False, null=False)
    content = BBCodeTextField(max_length=280, blank=False, null=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.user)
