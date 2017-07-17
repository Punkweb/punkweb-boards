from django.contrib import admin
from apps.api.models import (
    EmailUser, Category, Subcategory, Thread, Post, Shout, Conversation,
    Message, Report, Notification)


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    ordering = ('order',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    list_display = ('name', 'order',)
    ordering = ('order',)


class PostInline(admin.TabularInline):
    model = Post
    ordering = ('created',)


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]
    list_display = ('title', 'category', 'user')
    ordering = ('title',)


class MessageInline(admin.TabularInline):
    model = Message
    fields = ('user', 'content',)
    ordering = ('created',)


class ConversationAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ('subject',)
    ordering = ('created',)


admin.site.register(EmailUser)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Report)
admin.site.register(Shout)
admin.site.register(Notification)
