from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin
from django.db import models
from precise_bbcode.fields import BBCodeTextField
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey


def get_placeholder_url():
	url = '{}placeholder_profile.png'.format(settings.STATIC_URL)
	return url


class EmailUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **kwargs):
		user = self.model(email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, username, password=None, **kwargs):
		user = self.create_user(email, username, password, **kwargs)
		user.is_admin = True
		user.save()
		return user


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


class EmailUser(AbstractBaseUser, UUIDPrimaryKey, CreatedModifiedMixin,
				PermissionsMixin, AvatarImagesMixin):
	GENDER_CHOICES = [
		('f', 'Female'),
		('m', 'Male'),
	]
	email = models.EmailField(unique=True, blank=False)
	username = models.CharField(max_length=16, unique=True, blank=False)
	image = ThumbnailerImageField(
		upload_to="user_images", null=True, blank=True)
	signature = BBCodeTextField(max_length=140, blank=True, null=True)
	gender = models.CharField(null=True, blank=True, max_length=1,
		choices=GENDER_CHOICES, default=None)
	birthdate = models.DateField(
		null=True, blank=True, verbose_name='Birth date')

	# special rights
	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	objects = EmailUserManager()

	def __str__(self):
		return self.username

	@property
	def num_posts(self):
		return len(self.threads.all()) + len(self.posts.all())

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def is_staff(self):
		return self.is_admin

	def is_superuser(self):
		return self.is_admin

	def has_perm(self, obj=None):
		return self.is_admin

	def has_perms(self, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin
