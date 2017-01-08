import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin
from django.db import models
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
from precise_bbcode.fields import BBCodeTextField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey


def get_placeholder_url():
	url = '{}placeholder_profile.png'.format(settings.STATIC_URL)
	return url

def user_image_file_name(instance, filename):
	folder = instance.username
	ext = (filename.split('.')[-1]).lower()
	filename = '{}.{}'.format(instance.username, ext)
	return '/'.join(['user_images', folder, filename])


class AvatarImagesMixin(models.Model):
	@property
	def avatar(self):
		if not self.image:
			return get_placeholder_url()
		else:
			return self.image['avatar'].url

	@property
	def avatar_small(self):
		if not self.image:
			return get_placeholder_url()
		else:
			return self.image['avatar_small'].url

	@property
	def avatar_smaller(self):
		if not self.image:
			return get_placeholder_url()
		else:
			return self.image['avatar_smaller'].url

	@property
	def avatar_smallest(self):
		if not self.image:
			return get_placeholder_url()
		else:
			return self.image['avatar_smallest'].url

	class Meta:
		abstract = True


class EmailUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **kwargs):
		user = self.model(email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, username, password=None, **kwargs):
		user = self.create_user(email, username, password, **kwargs)
		user.is_superuser = True
		user.save()
		return user


class EmailUser(AbstractBaseUser, UUIDPrimaryKey, CreatedModifiedMixin,
				PermissionsMixin, AvatarImagesMixin):
	GENDER_CHOICES = [
		('f', 'Female'),
		('m', 'Male'),
	]
	email = models.EmailField(unique=True, blank=False)
	username = models.CharField(max_length=16, unique=True, blank=False)
	image = ThumbnailerImageField(
		upload_to=user_image_file_name, null=True, blank=True)
	signature = BBCodeTextField(max_length=140, blank=True, null=True)
	gender = models.CharField(null=True, blank=True, max_length=1,
		choices=GENDER_CHOICES, default=None)
	birthday = models.DateField(
		null=True, blank=True, verbose_name='Birth date')

	is_banned = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	objects = EmailUserManager()

	def __str__(self):
		return self.username

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	@property
	def is_staff(self):
		return self.is_superuser

	@property
	def num_posts(self):
		return len(self.threads.all()) + len(self.posts.all())

	@property
	def age(self):
		# Ugly but hey, it works.
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

	def get_absolute_url(self):
		return reverse('board:profile', self.username)


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
        if self.admin_req and user.is_authenticated and user.is_staff:
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
    pinned = models.BooleanField(default=False)

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
        return Post.objects.filter(thread__id=self.id).select_related()

    @property
    def posts_count(self):
        return len(self.posts.all())

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
            self.user, self.thread, self.created.strftime("%Y-%m-%d %H:%M"))

    def can_edit(self, user):
        if user.is_authenticated and user.is_banned:
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
    reporting_user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='reports_created', blank=False, null=False)
    reason = models.TextField(max_length=1024, blank=False, null=False)
    thread = models.ForeignKey(Thread, blank=True, null=True, default=None)
    post = models.ForeignKey(Post, blank=True, null=True, default=None)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='reports_resolved', blank=True, null=True)
    date_resolved = models.DateTimeField(blank=True, null=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    content = BBCodeTextField(max_length=280, blank=False, null=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('board:index') # TODO Actual url
