from django.contrib import admin
from apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', )


admin.site.register(Page, PageAdmin)
