from django import forms
from django.contrib import admin
from apps.pages.models import Page


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


admin.site.register(Page, PageAdmin)
