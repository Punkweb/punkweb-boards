from django.db import models
from django.utils.text import slugify
from precise_bbcode.fields import BBCodeTextField
from apps.api.mixins import UUIDPrimaryKey, CreatedModifiedMixin


class Page(models.Model):
    slug = models.SlugField(max_length=140, unique=True)
    title = models.CharField(max_length=256)
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
