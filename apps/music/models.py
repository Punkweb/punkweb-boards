from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField
from precise_bbcode.fields import BBCodeTextField

from apps.common.models import (UploadedAtMixin, CreatedModifiedMixin,
                                UUIDPrimaryKey)


def audio_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'audio', filename])


def audio_compilation_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'compilations', filename])


def artist_image_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'artists', filename])


def album_cover_upload_to(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = '{}.{}'.format(instance.slug, ext)
    return '/'.join(['music', 'album', filename])


class Artist(UUIDPrimaryKey):
    slug = models.SlugField(
        max_length=256, blank=False, null=False, unique=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    genre = models.CharField(max_length=256)
    bio = BBCodeTextField(max_length=5096, blank=True, null=True)
    image = ThumbnailerImageField(
        upload_to=artist_image_upload_to, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Album(UUIDPrimaryKey):
    slug = models.SlugField(max_length=256, blank=False, null=False, unique=True)
    artist = models.ForeignKey('Artist',
        blank=False, null=False, related_name='albums')
    title = models.CharField(max_length=256, blank=False, null=False)
    year = models.DateField()
    cover_art = ThumbnailerImageField(
        upload_to=album_cover_upload_to, blank=True, null=True)
    genre = models.CharField(max_length=256)

    class Meta:
        ordering = ('artist', 'title', 'year',)

    def __str__(self):
        return '{}: {}'.format(self.artist.name, self.title)


class TrackInformationMixin(models.Model):
    slug = models.SlugField(max_length=256, blank=False, null=False, unique=True)
    title = models.CharField(max_length=256, blank=False, null=False)
    album = models.ForeignKey('Album',
        blank=True, null=True, related_name='tracks')
    disc_num = models.IntegerField()
    track_num = models.IntegerField()

    class Meta:
        abstract = True


class Audio(UUIDPrimaryKey, UploadedAtMixin, TrackInformationMixin):
    file = models.FileField(upload_to=audio_upload_to, blank=False, null=False)

    class Meta:
        ordering = (
            'album__artist__name', 'album__title', 'disc_num', 'track_num', 'title',)

    def __str__(self):
        return '{} - {} - {}'.format(self.title,
            self.album.artist.name, self.album.title)


class AudioCompilation(UUIDPrimaryKey, CreatedModifiedMixin):
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=256, blank=False, null=False)
    thumbnail = ThumbnailerImageField(
        upload_to=audio_compilation_upload_to, blank=True, null=True)
    tracks = models.ManyToManyField(Audio)

    def __str__(self):
        return '{} - {}'.format(self.created, self.title)
