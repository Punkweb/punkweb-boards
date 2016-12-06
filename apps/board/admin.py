from django.contrib import admin
from django_markdown.admin import MarkdownField, AdminMarkdownWidget
from apps.board.models import ParentCategory, ChildCategory, Post, Comment


class ChildCategoryInline(admin.TabularInline):
    model = ChildCategory
    ordering = ('order', )


class ParentCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ChildCategoryInline,
    ]
    list_display = ('name', 'order', )
    ordering = ('order', )


# class ChildCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'order', )
#     ordering = ('order', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user')
    ordering = ('title', )
    formfield_overrides = {
        MarkdownField: {
            'widget': AdminMarkdownWidget
        }
    }


admin.site.register(ParentCategory, ParentCategoryAdmin)
# admin.site.register(ChildCategory, ChildCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
