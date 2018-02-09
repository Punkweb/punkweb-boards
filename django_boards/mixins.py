import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from easy_thumbnails.files import get_thumbnailer
from django_boards import utils


class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UploadedAtMixin(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDPrimaryKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UpvoteDownvoteMixin(models.Model):
    upvoted_by = models.ManyToManyField(
        get_user_model(), related_name='%(app_label)s_%(class)s_upvoted',
        blank=True)
    downvoted_by = models.ManyToManyField(
        get_user_model(), related_name='%(app_label)s_%(class)s_downvoted',
        blank=True)

    class Meta:
        abstract = True


class AvatarImagesMixin(models.Model):
    @property
    def avatar(self):
        if not self.image:
            if utils.has_gravatar(self.user.email):
                return utils.get_gravatar_url(self.user.email, size=200)
            return get_thumbnailer(utils.get_placeholder_url())['avatar'].url
        else:
            return self.image['avatar'].url

    @property
    def avatar_small(self):
        if not self.image:
            if utils.has_gravatar(self.user.email):
                return utils.get_gravatar_url(self.user.email, size=100)
            return get_thumbnailer(utils.get_placeholder_url())['avatar_small'].url
        else:
            return self.image['avatar_small'].url

    @property
    def avatar_smaller(self):
        if not self.image:
            if utils.has_gravatar(self.user.email):
                return utils.get_gravatar_url(self.user.email, size=50)
            return get_thumbnailer(utils.get_placeholder_url())['avatar_smaller'].url
        else:
            return self.image['avatar_smaller'].url

    @property
    def avatar_smallest(self):
        if not self.image:
            if utils.has_gravatar(self.user.email):
                return utils.get_gravatar_url(self.user.email, size=25)
            return get_thumbnailer(utils.get_placeholder_url())['avatar_smallest'].url
        else:
            return self.image['avatar_smallest'].url

    class Meta:
        abstract = True
