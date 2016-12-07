from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django_markdown.models import MarkdownField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey


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


class EmailUser(AbstractBaseUser, UUIDPrimaryKey, CreatedModifiedMixin,
				PermissionsMixin):
	GENDER_CHOICES = [
		('f', 'Female'),
		('m', 'Male'),
	]
	email = models.EmailField(unique=True, blank=False)
	username = models.CharField(max_length=16, unique=True, blank=False)
	image = models.ImageField(upload_to="user_images", null=True, blank=True)
	signature = MarkdownField()
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
