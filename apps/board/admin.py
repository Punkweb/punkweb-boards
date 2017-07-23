from django.contrib import admin
from apps.api.models import (
    EmailUser, Category, Subcategory, Thread, Post, Shout, Conversation,
    Message, Report, Notification, UserRank)


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
    fields = (
        'user', 'category', 'title', 'content', 'modified', 'created',
        'pinned', 'closed', 'tags', 'upvoted_by', 'downvoted_by',)
    readonly_fields = (
        'modified', 'created',)


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


class EmailUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rank', 'is_superuser',)
    ordering = ('username',)
    fields = (
        'username', 'email', 'gender', 'birthday', 'rank', 'is_superuser',
        'is_banned', 'last_login', 'image', 'avatar_thumbnail', 'signature',
        'rendered_signature', 'username_modifier', 'rendered_username', )
    readonly_fields = (
        'avatar_thumbnail', 'rendered_signature', 'rendered_username', )


class UserRankAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('order',)
    fields = (
        'title', 'description', 'order', 'username_modifier', 'example_name',)
    readonly_fields = ('example_name',)


admin.site.register(EmailUser, EmailUserAdmin)
admin.site.register(UserRank, UserRankAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Report)
admin.site.register(Shout)
admin.site.register(Notification)
