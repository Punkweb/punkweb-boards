import uuid
from django.conf import settings
from django.db import models


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
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UpvoteDownvoteMixin(models.Model):
    upvoted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_upvoted',
        blank=True)
    downvoted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_downvoted',
        blank=True)

    class Meta:
        abstract = True
