from django import forms
from django.contrib import admin

from punkweb_boards.models import (
    BoardProfile,
    Category,
    Subcategory,
    Thread,
    Post,
    Shout,
    Conversation,
    Message,
    Report,
    Notification,
    UserRank,
    Page,
)

JAVASCRIPT_FILES = (
    "punkweb_boards/js/deps/jquery-3.6.0.min.js",
    "punkweb_boards/js/deps/run-prettify.js",
    "punkweb_boards/js/deps/sceditor-3.1.1/minified/jquery.sceditor.bbcode.min.js",
    "punkweb_boards/js/deps/sceditor-3.1.1/minified/icons/material.js",
    "punkweb_boards/js/editor-config.js",
)

CSS_FILES = ("punkweb_boards/js/deps/sceditor-3.1.1/minified/themes/square.min.css",)


# Forms


class BoardProfileForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        widgets = {
            "signature": forms.Textarea(attrs={"class": "post-editor"}),
            "username_modifier": forms.Textarea(attrs={"class": "post-editor"}),
        }
        fields = "__all__"


class UserRankForm(forms.ModelForm):
    class Meta:
        model = UserRank
        widgets = {"username_modifier": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {"description": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        widgets = {"description": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        widgets = {"content": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {"content": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        widgets = {"content": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {"content": forms.Textarea(attrs={"class": "post-editor"})}
        fields = "__all__"


# ModelAdmin


class BoardProfileAdmin(admin.ModelAdmin):
    form = BoardProfileForm
    list_display = [
        "username",
        "last_seen",
        "post_count",
        "rank_title",
    ]
    list_filter = [
        "user__is_active",
        "user__is_staff",
        "user__is_superuser",
        "is_banned",
        "ranks",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]
    fields = [
        "username",
        "image",
        "avatar_thumbnail",
        "gender",
        "birthday",
        "is_banned",
        "ranks",
        "username_modifier",
        "rendered_username",
        "signature",
        "rendered_signature",
    ]
    readonly_fields = [
        "username",
        "avatar_thumbnail",
        "rendered_signature",
        "rendered_username",
    ]

    def username(self, obj):
        return obj.user.username

    username.short_description = "username"
    username.admin_order_field = "user__username"

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class UserRankAdmin(admin.ModelAdmin):
    form = UserRankForm
    list_display = [
        "title",
        "order",
        "is_award",
        "award_type",
        "award_count",
    ]
    list_filter = [
        "is_award",
        "award_type",
    ]
    search_fields = [
        "title",
        "description",
    ]
    fields = [
        "title",
        "description",
        "order",
        "is_award",
        "award_type",
        "award_count",
        "username_modifier",
        "example_name",
    ]
    readonly_fields = [
        "example_name",
    ]

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    form = SubcategoryForm

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    inlines = [SubcategoryInline]
    list_display = [
        "name",
        "order",
        "auth_req",
    ]
    list_filter = [
        "auth_req",
    ]
    search_fields = [
        "name",
        "description",
    ]

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class PostInline(admin.TabularInline):
    form = PostForm
    model = Post
    ordering = ("created",)
    fields = ("user", "content", "upvoted_by", "downvoted_by")

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class ThreadAdmin(admin.ModelAdmin):
    form = ThreadForm
    inlines = [PostInline]
    list_display = [
        "title",
        "category",
        "user",
        "created",
        "pinned",
        "closed",
    ]
    fields = [
        "user",
        "category",
        "title",
        "content",
        "modified",
        "created",
        "pinned",
        "closed",
        "tags",
        "upvoted_by",
        "downvoted_by",
    ]
    readonly_fields = [
        "modified",
        "created",
    ]

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class MessageInline(admin.TabularInline):
    form = MessageForm
    model = Message
    fields = [
        "user",
        "content",
    ]

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class ConversationAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = [
        "subject",
        "message_count",
    ]
    search_fields = [
        "subject",
    ]

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "reporting_user",
        "thread",
        "post",
        "resolved",
        "resolved_by",
        "date_resolved",
    ]
    list_filter = [
        "resolved",
    ]
    search_fields = [
        "reporting_user__username",
        "reporting_user__email",
    ]
    readonly_fields = [
        "created",
        "modified",
    ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "link",
        "created",
        "read",
    ]
    list_filter = [
        "created",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = [
        "title",
        "slug",
    ]
    search_fields = [
        "title",
    ]
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = JAVASCRIPT_FILES
        css = {"all": CSS_FILES}


admin.site.register(BoardProfile, BoardProfileAdmin)
admin.site.register(UserRank, UserRankAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Shout)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Page, PageAdmin)
