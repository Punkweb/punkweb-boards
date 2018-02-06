from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.urls import resolve, reverse
from precise_bbcode.fields import BBCodeTextField
from apps.api.mixins import UUIDPrimaryKey, CreatedModifiedMixin


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
