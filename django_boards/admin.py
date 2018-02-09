from django import forms
from django.contrib import admin

from django_boards.models import (
    BoardProfile, Category, Subcategory, Thread, Post, Shout, Conversation,
    Message, Report, Notification, UserRank, Page)


# Forms

class BoardProfileForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        widgets = {
            'signature': forms.Textarea(attrs={'class': 'post-editor'}),
            'username_modifier': forms.Textarea(attrs={'class': 'post-editor'}),
        }
        fields = ('__all__')


class UserRankForm(forms.ModelForm):
    class Meta:
        model = UserRank
        widgets = {
            'username_modifier': forms.Textarea(attrs={'class': 'post-editor'}),
        }
        fields = ('__all__')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {
            'description': forms.Textarea(attrs={'class': 'post-editor'})
        }
        fields = ('__all__')


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        widgets = {
            'description': forms.Textarea(attrs={'class': 'post-editor'})
        }
        fields = ('__all__')


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        widgets = {
            'content': forms.Textarea(attrs={'class': 'post-editor'})
        }
        fields = ('__all__')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'content': forms.Textarea(attrs={'class': 'post-editor'})
        }
        fields = ('__all__')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        widgets = {
            'content': forms.Textarea(attrs={'class': 'post-editor'})
        }
        fields = ('__all__')


# ModelAdmin

class BoardProfileAdmin(admin.ModelAdmin):
    form = BoardProfileForm
    list_display = ('get_username', 'get_email',)
    ordering = ('user__username',)
    fields = (
        'get_username', 'get_email', 'gender', 'birthday', 'ranks', 'is_banned',
        'image', 'avatar_thumbnail', 'signature', 'rendered_signature',
        'username_modifier', 'rendered_username',)
    readonly_fields = (
        'get_username', 'get_email', 'avatar_thumbnail', 'rendered_signature',
        'rendered_username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'


class UserRankAdmin(admin.ModelAdmin):
    form = UserRankForm
    list_display = ('title', 'order', 'is_award', 'award_type', 'award_count', )
    ordering = ('order', )
    fields = (
        'title', 'description', 'order', 'is_award', 'award_type', 'award_count',
        'username_modifier', 'example_name', )
    readonly_fields = ('example_name',)


class SubcategoryInline(admin.TabularInline):
    form = SubcategoryForm
    model = Subcategory
    ordering = ('order',)


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    inlines = [
        SubcategoryInline,
    ]
    list_display = ('name', 'order',)
    ordering = ('order',)


class PostInline(admin.TabularInline):
    form = PostForm
    model = Post
    ordering = ('created',)
    fields = (
        'user', 'content', 'upvoted_by', 'downvoted_by',)


class ThreadAdmin(admin.ModelAdmin):
    form = ThreadForm
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
    form = MessageForm
    model = Message
    fields = ('user', 'content',)
    ordering = ('created',)


class ConversationAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ('subject',)
    ordering = ('created',)


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


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'content': forms.Textarea(attrs={'class': 'post-editor'}),
        }
        fields = ('__all__')


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('title', 'slug', )
    prepopulated_fields = {
        'slug': ('title', )
    }

admin.site.register(BoardProfile, BoardProfileAdmin)
admin.site.register(UserRank, UserRankAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Shout)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Page, PageAdmin)
