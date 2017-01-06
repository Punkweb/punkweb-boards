import datetime
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
