import datetime
import hashlib
import math
import base64
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
from precise_bbcode.fields import BBCodeTextField

from django_boards import utils
from django_boards.conf import settings as BOARD_SETTINGS
from django_boards.mixins import (
    CreatedModifiedMixin, UUIDPrimaryKey, UpvoteDownvoteMixin,
    AvatarImagesMixin,)


def profile_image_file_name(instance, filename):
    folder = instance.user.username
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.user.username, ext)
    return '/'.join(['user_images', folder, filename])


class BoardProfile(CreatedModifiedMixin, UUIDPrimaryKey, UpvoteDownvoteMixin,
                   AvatarImagesMixin):
    GENDER_CHOICES = [
        ('f', 'Female'),
        ('m', 'Male'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    image = ThumbnailerImageField(
        upload_to=profile_image_file_name, null=True, blank=True)
    signature = BBCodeTextField(max_length=1024, blank=True, null=True)
    gender = models.CharField(
        null=True, blank=True, max_length=1, choices=GENDER_CHOICES, default=None)
    birthday = models.DateField(
        null=True, blank=True, verbose_name='Birth date')
    is_banned = models.BooleanField(default=False)
    ranks = models.ManyToManyField('UserRank', blank=True)
    username_modifier = models.TextField(
        max_length=250, blank=True, null=True,
        help_text="BBCode. Just add {USER} where " \
                  "you want the username to be placed at. " \
                  "Setting this will override the UserRank modification")

    def last_seen(self):
        name = self.user.username.replace(' ', '_')
        return cache.get('seen_%s' % name)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + \
                datetime.timedelta(seconds=BOARD_SETTINGS.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    @property
    def post_count(self):
        return len(self.user.threads.all()) + len(self.user.posts.all())

    @property
    def age(self):
        if not self.birthday:
            return 0
        today = datetime.date.today()
        return (today.year - self.birthday.year -
                ((today.month, today.day) <
                 (self.birthday.month, self.birthday.day)))

    @property
    def birthday_today(self):
        if self.birthday is None:
            return False
        today = datetime.date.today()
        match = self.birthday.day == today.day and \
                self.birthday.month == today.month
        if match:
            return True
        return False

    @property
    def can_shout(self):
        if not BOARD_SETTINGS.SHOUTBOX_ENABLED:
            return False
        if BOARD_SETTINGS.SHOUTBOX_MINIMUM_POSTS:
            has_post_req = self.post_count >= BOARD_SETTINGS.SHOUTBOX_MINIMUM_POSTS_REQ
            if not has_post_req:
                return False
        return True

    @property
    def rank(self):
        if not self.ranks:
            return None
        return self.ranks.order_by('order').first()

    @property
    def rank_title(self):
        if not self.rank:
            return 'Rookie'
        else:
            return self.rank.title

    @property
    def rendered_username(self):
        return utils.render_username(self)

    @property
    def rendered_rank(self):
        if not self.rank:
            name = 'Rookie'
        else:
            name = self.rank.title
        return utils.render_example_username(self.rank, name)

    @property
    def rendered_signature(self):
        """Used on admin page"""
        return mark_safe(self.signature.rendered)

    @property
    def avatar_thumbnail(self):
        """Returns html tag with user image. Used on admin page"""
        return mark_safe('<img src="{}" />'.format(self.avatar_small))

    def get_absolute_url(self):
        return reverse('board:profile', self.user.username)


class UserRank(models.Model):
    AWARD_TYPE_CHOICES = (
        ('post_count', 'Post Count'),
    )
    title = models.CharField(max_length=96, blank=False, null=False, unique=True)
    description = models.TextField(max_length=256, blank=True, null=True)
    order = models.IntegerField(
        help_text='Where this rank ranks among the other ranks')
    is_award = models.BooleanField(default=False)
    award_type = models.CharField(
        max_length=50, choices=AWARD_TYPE_CHOICES, null=True, blank=True, default=None)
    award_count = models.IntegerField(default=0, null=True, blank=True)
    username_modifier = models.TextField(
        max_length=250, blank=True, null=True,
        help_text="BBCode. Just add {USER} where "\
                  "you want the username to be placed at.")

    @property
    def example_name(self):
        return utils.render_example_username(self, self.title)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title

class Category(UUIDPrimaryKey):
    name = models.CharField(max_length=96, blank=False, null=False, unique=True)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()
    auth_req = models.BooleanField(
        default=False, help_text='Can only logged in users view this category?')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('order',)

    def __str__(self):
        return "{}. {}".format(self.order, self.name)

    def can_view(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if not user.is_authenticated and self.auth_req:
            return False
        return True

    @property
    def subcategories(self):
        return Subcategory.objects.filter(parent__id=self.id)

    def get_absolute_url(self):
        return reverse('board:category', kwargs={'pk': self.id})


class Subcategory(UUIDPrimaryKey):
    parent = models.ForeignKey(
        Category, blank=True, null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=96, blank=False, null=False)
    description = BBCodeTextField(max_length=256, blank=True, null=True)
    order = models.IntegerField()
    staff_req = models.BooleanField(default=False,
        help_text='Can only staff members can create threads in this subcategory?')
    auth_req = models.BooleanField(default=False,
       help_text='Can only logged in users view this subcategory?')

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        ordering = ('parent__order', 'order',)

    def __str__(self):
        return "{} > {}. {}".format(self.parent, self.order, self.name)

    def can_view(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if not user.is_authenticated and self.auth_req:
            return False
        if not user.is_authenticated and self.parent.auth_req:
            return False
        return True

    def can_post(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if self.staff_req and user.is_authenticated and user.is_staff:
            return True
        if not self.staff_req and user.is_authenticated:
            return True
        return False

    @property
    def threads(self):
        return Thread.objects.filter(category__id=self.id)

    @property
    def thread_count(self):
        return len(self.threads)

    @property
    def posts(self):
        return Post.objects.filter(thread__category__id=self.id)

    @property
    def post_count(self):
        return len(self.posts)

    @property
    def last_thread(self):
        return self.threads.order_by('-created').first()

    def get_absolute_url(self):
        return reverse('board:subcategory', kwargs={'pk': self.id})


class Thread(CreatedModifiedMixin, UUIDPrimaryKey, UpvoteDownvoteMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='threads', blank=False,
        null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Subcategory, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, null=False)
    content = BBCodeTextField(max_length=30000, blank=False, null=False)
    pinned = models.BooleanField(default=False)
    closed = models.BooleanField(
        default=False,
        help_text="Check to stop users from being able " \
                  "to comment on this thread."
    )
    # TODO: Better tagging in the future.
    tags = models.CharField(
        max_length=1024, blank=True, null=True,
        help_text="Optional. Improves keywoard searching. " \
                  "Separate tags with a comma and space. " \
                  "(eg. news, important, update)")

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} by {}'.format(self.title, self.user)

    def can_view(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if self.category.auth_req and not user.is_authenticated:
            return False
        if self.category.parent.auth_req and not user.is_authenticated:
            return False
        return True

    def can_edit(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if user.is_authenticated and user.is_staff:
            return True
        if self.user.id == user.id:
            return True
        return False

    @property
    def reported(self):
        if len(Report.objects.filter(thread__id=self.id, resolved=False)) >= 1:
            return True
        else:
            return False

    @property
    def posts(self):
        return Post.objects.filter(thread__id=self.id)

    @property
    def posts_count(self):
        return len(self.posts.all())

    @property
    def last_post(self):
        return self.posts.order_by('created').first()

    @property
    def upvotes(self):
        return len(self.upvoted_by.all())

    @property
    def downvotes(self):
        return len(self.downvoted_by.all())

    def get_absolute_url(self):
        return reverse('board:thread', kwargs={'pk': self.id})


class Post(CreatedModifiedMixin, UUIDPrimaryKey, UpvoteDownvoteMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts', blank=False, null=False,
        on_delete=models.CASCADE)
    thread = models.ForeignKey(
        Thread, related_name='posts', blank=False, null=False,
        on_delete=models.CASCADE)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}\'s post on {}, {}'.format(
            self.user, self.thread, self.created.strftime("%Y-%m-%d %H:%M"))

    def can_edit(self, user):
        if user.is_authenticated and user.profile.is_banned:
            return False
        if user.is_authenticated and user.is_staff:
            return True
        if self.user.id == user.id:
            return True
        return False

    @property
    def reported(self):
        if len(Report.objects.filter(post__id=self.id, resolved=False)) >= 1:
            return True
        else:
            return False

    @property
    def post_number(self):
        qs = self.thread.posts.order_by('created')
        post_index = list(qs.values_list('id', flat=True)).index(self.id)
        return post_index + 1

    @property
    def page_number(self, page_size=10):
        return math.ceil(self.post_number / page_size)

    @property
    def upvotes(self):
        return len(self.upvoted_by.all())

    @property
    def downvotes(self):
        return len(self.downvoted_by.all())

    def get_absolute_url(self):
        return '/board/thread/{}/?page={}#p{}'.format(
            self.thread.id, self.page_number, self.post_number)


class Conversation(UUIDPrimaryKey, CreatedModifiedMixin):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='conversations')
    subject = models.TextField(
        max_length=140, blank=True, null=True, default='No subject')
    unread_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='unread_conversations', blank=True)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return self.subject

    # @property
    # def messages(self):
    #     return Message.objects.filter(conversation__id=self.id)

    @property
    def message_count(self):
        return len(self.messages.all())

    @property
    def last_message(self):
        return self.messages.order_by('-created').first()

    def get_absolute_url(self):
        return reverse('board:conversation', kwargs={'pk': self.id})


class Message(UUIDPrimaryKey, CreatedModifiedMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages',
        on_delete=models.CASCADE)
    content = BBCodeTextField(max_length=10000, blank=False, null=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('board:conversation', kwargs={'pk': self.convseration.id})


class Report(CreatedModifiedMixin, UUIDPrimaryKey):
    reporting_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reports_created', blank=False,
        null=False, on_delete=models.CASCADE)
    reason = models.TextField(max_length=1024, blank=False, null=False)
    thread = models.ForeignKey(
        Thread, blank=True, null=True, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, blank=True, null=True, default=None, on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reports_resolved', blank=True,
        null=True, on_delete=models.CASCADE)
    date_resolved = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.thread:
            in_question = self.thread
        if self.post:
            in_question = self.post
        return '{}\'s report on {}'.format(
            self.reporting_user.username, in_question)

    def get_absolute_url(self):
        return reverse('board:report', self.id)


class Shout(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.CASCADE)
    content = BBCodeTextField(max_length=280, blank=False, null=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('board:index')


class Notification(CreatedModifiedMixin, UUIDPrimaryKey):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, null=False,
        related_name='notifications', on_delete=models.CASCADE)
    text = models.CharField(max_length=140, blank=False, null=False)
    link = models.CharField(max_length=140, blank=False, null=False)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.text


class Page(UUIDPrimaryKey, CreatedModifiedMixin):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=140, unique=True,
        help_text="The url that this page will be at: /board/pages/{{slug}}")
    content = BBCodeTextField(max_length=50000, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(self.id,))

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug': self.slug})


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        BoardProfile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Thread)
@receiver(post_save, sender=Post)
def thread_notifications(sender, instance, created, **kwargs):
    if created:
        # Award ranks if applicable
        awardable_ranks = UserRank.objects.filter(
            is_award=True, award_type='post_count')
        for rank in awardable_ranks:
            if instance.user.profile.post_count >= rank.award_count:
                instance.user.profile.ranks.add(rank)
                instance.user.profile.save()
        # Send notification to tagged users
        content = str(instance.content)
        tagged_users = utils.tagged_usernames(content)
        for user in tagged_users:
            try:
                user_obj = get_user_model().objects.get(username=user)
            except Exception as e:
                user_obj = None
            if user_obj:
                notification = Notification(
                    user=user_obj,
                    text='{} tagged you in a post.'.format(
                        instance.user.username),
                    link=instance.get_absolute_url(),
                    read=False
                )
                notification.save()
