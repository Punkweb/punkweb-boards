from django.contrib import admin
from django.contrib.admin.models import LogEntry

from apps.api.models import (
    EmailUser, Category, Subcategory, Thread, Post, Shout, Conversation,
    Message, Report, Notification, UserRank)


class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


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
    fields = (
        'user', 'content', 'upvoted_by', 'downvoted_by',)


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]
    list_display = ('title', 'category', 'user', 'created', )
    ordering = ('-created', 'title',)
    fields = (
        'user', 'category', 'title', 'content', 'modified', 'created',
        'pinned', 'closed', 'tags', 'upvoted_by', 'downvoted_by',)
    readonly_fields = ('modified', 'created',)


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
        'admin_access', 'is_banned', 'groups', 'user_permissions',
        'last_login', 'image', 'avatar_thumbnail', 'signature',
        'rendered_signature', 'username_modifier', 'rendered_username',)
    readonly_fields = (
        'avatar_thumbnail', 'rendered_signature', 'rendered_username',)


class UserRankAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('order',)
    fields = (
        'title', 'description', 'order', 'username_modifier', 'example_name',)
    readonly_fields = ('example_name',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporting_user', 'thread', 'post', 'resolved', )
    ordering = ('-created',)
    fields = (
        'reporting_user', 'thread', 'post', 'reason', 'created', 'modified',
        'resolved', 'resolved_by', 'date_resolved', )
    readonly_fields = ('created', 'modified', )


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'link', 'created', 'read',)
    ordering = ('-created', )


admin.site.site_header = 'Punk Web'
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(EmailUser, EmailUserAdmin)
admin.site.register(UserRank, UserRankAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Shout)
admin.site.register(Notification)
