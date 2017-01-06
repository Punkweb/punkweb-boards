from django.conf import settings
from django.db import models
from django.urls import reverse
from precise_bbcode.fields import BBCodeTextField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey


class Category(UUIDPrimaryKey):
    name = models.CharField(max_length=96, blank=False, null=False, unique=True)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()
    auth_req = models.BooleanField(default=False,
        help_text='Can only logged in users view this category?')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('order', )

    def __str__(self):
        return "{}. {}".format(self.order, self.name)

    def can_view(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if not user.is_authenticated and self.auth_req:
            return False
        return True

    @property
    def subcategories(self):
        return Subcategory.objects.filter(
            parent__id=self.id).select_related()

    def get_absolute_url(self):
        return reverse('board:category', kwargs={'pk': self.id})


class Subcategory(UUIDPrimaryKey):
    parent = models.ForeignKey(
        Category, blank=True, null=True, default=None)
    name = models.CharField(max_length=96, blank=False, null=False)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()
    admin_req = models.BooleanField(default=False,
        help_text='Can only admin users create threads in this subcategory?')
    auth_req = models.BooleanField(default=False,
        help_text='Can only logged in users view this subcategory?')

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        ordering = ('order', )

    def __str__(self):
        return "{}. {}".format(self.order, self.name)

    def can_view(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if not user.is_authenticated and self.auth_req:
            return False
        return True

    def can_post(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if self.admin_req and user.is_authenticated and user.is_admin:
            return True
        if not self.admin_req and user.is_authenticated:
            return True
        return False

    @property
    def threads(self):
        return Thread.objects.filter(
            category__id=self.id).select_related()

    @property
    def posts(self):
        return Post.objects.filter(
            thread__category__id=self.id).select_related()

    @property
    def last_thread(self):
        return self.threads.order_by('-created').first()

    def get_absolute_url(self):
        return reverse('board:subcategory', kwargs={'pk': self.id})


class Thread(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='threads', blank=False, null=False)
    category = models.ForeignKey(Subcategory, blank=False, null=False)
    title = models.CharField(max_length=96, blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return '{}, {}'.format(self.title, self.created)

    def can_view(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if self.category.auth_req and not user.is_authenticated:
            return False
        return True

    def can_edit(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if user.is_authenticated and user.is_admin:
            return True
        if self.user.id == user.id:
            return True
        return False

    @property
    def reported(self):
        if len(Report.objects.filter(thread__id=self.id, closed=False)) >= 1:
            return True
        else:
            return False

    @property
    def posts(self):
        return Post.objects.filter(thread__id=self.id).select_related()

    @property
    def last_post(self):
        return self.posts.order_by('-created').first()

    def get_absolute_url(self):
        return reverse('board:thread', kwargs={'pk': self.id})


class Post(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts', blank=False, null=False)
    thread = models.ForeignKey(
        Thread, related_name='posts', blank=False, null=False)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    def __str__(self):
        return '{}\'s post on {} {}'.format(
            self.user, self.thread, self.created)

    def can_edit(self, user):
        if user.is_authenticated and user.is_banned:
            return False
        if user.is_authenticated and user.is_admin:
            return True
        if self.user.id == user.id:
            return True
        return False

    @property
    def reported(self):
        if len(Report.objects.filter(post__id=self.id, closed=False)) >= 1:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('board:thread', kwargs={'pk': self.thread.id})


class Conversation(UUIDPrimaryKey, CreatedModifiedMixin):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='conversations')
    subject = models.TextField(
        max_length=140, blank=True, null=True, default='No subject')
    unread_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='unread_conversations')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('board:messages') # TODO Actual url


class Message(UUIDPrimaryKey, CreatedModifiedMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, related_name='messages')
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('board:messages') # TODO Actual url


class Report(CreatedModifiedMixin, UUIDPrimaryKey):
    reporting_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, null=False)
    reason = models.TextField(max_length=1024, blank=False, null=False)
    thread = models.ForeignKey(Thread, blank=True, null=True, default=None)
    post = models.ForeignKey(Post, blank=True, null=True, default=None)
    closed = models.BooleanField(default=False)

    def __str__(self):
        if thread:
            in_question = thread
        if post:
            in_question = post
        return '{}\'s report on {}'.format(reporting_user.username, in_question)


class Shout(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    content = BBCodeTextField(max_length=280, blank=False, null=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.user)
