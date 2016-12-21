from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    fields = ('user', 'content',)
    ordering = ('created', )


class ConversationAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ('subject', )
    ordering = ('created', )


admin.site.register(Conversation, ConversationAdmin)
