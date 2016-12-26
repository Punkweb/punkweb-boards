from django.db import models
from django.conf import settings
from django.urls import reverse, reverse_lazy
from precise_bbcode.fields import BBCodeTextField
from apps.common.models import CreatedModifiedMixin, UUIDPrimaryKey


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
        return reverse_lazy('board:index')


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
        return reverse_lazy('board:index')
