from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField

from apps.common.models import UploadedAtMixin, CreatedModifiedMixin, UUIDPrimaryKey


def video_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'videos', filename])


def audio_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'audio', filename])


def audio_compilation_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'compilations', 'audio', filename])


class TrackInformationMixin(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    artist = models.CharField(max_length=256, blank=False, null=False)
    album = models.CharField(max_length=256, blank=False, null=False)
    genre = models.CharField(max_length=256)
    year = models.DateField()
    disc = models.IntegerField()
    track = models.IntegerField()

    class Meta:
        abstract = True


class Video(UUIDPrimaryKey, UploadedAtMixin, TrackInformationMixin):
    slug = models.SlugField(max_length=256, blank=False, null=False)
    file = models.FileField(upload_to=video_upload_to, blank=False, null=False)
    thumbnail = ThumbnailerImageField(
        upload_to=video_upload_to, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.uploaded_at, self.title)


class Audio(UUIDPrimaryKey, UploadedAtMixin, TrackInformationMixin):
    slug = models.SlugField(max_length=256, blank=False, null=False)
    file = models.FileField(upload_to=audio_upload_to, blank=False, null=False)
    thumbnail = ThumbnailerImageField(
        upload_to=audio_upload_to, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.uploaded_at, self.title)


class AudioCompilation(UUIDPrimaryKey, CreatedModifiedMixin):
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=256, blank=False, null=False)
    thumbnail = ThumbnailerImageField(
        upload_to=audio_upload_to, blank=True, null=True)
    tracks = models.ManyToManyField(Audio)

    def __str__(self):
        return '{} - {}'.format(self.created, self.title)


class VideoCompilation(UUIDPrimaryKey, CreatedModifiedMixin):
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=256, blank=False, null=False)
    thumbnail = ThumbnailerImageField(
        upload_to=audio_upload_to, blank=True, null=True)
    tracks = models.ManyToManyField(Video)

    def __str__(self):
        return '{} - {}'.format(self.created, self.title)
