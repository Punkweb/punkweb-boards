from django.contrib import admin
from apps.board.models import Category, Subcategory, Thread, Post, Shout


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    ordering = ('order', )


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    list_display = ('name', 'order', )
    ordering = ('order', )


class PostInline(admin.TabularInline):
    model = Post
    ordering = ('created', )


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        PostInline
    ]
    list_display = ('title', 'category', 'user')
    ordering = ('title', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post)
admin.site.register(Shout)
