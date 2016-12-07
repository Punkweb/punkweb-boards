from django.contrib import admin
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

class CommentInline(admin.TabularInline):
    model = Comment
    ordering = ('created', )


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]
    list_display = ('title', 'category', 'user')
    ordering = ('title', )


admin.site.register(ParentCategory, ParentCategoryAdmin)
# admin.site.register(ChildCategory, ChildCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
