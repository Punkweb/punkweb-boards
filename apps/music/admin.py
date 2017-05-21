from django.contrib import admin
from . import models


class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'year', 'disc', 'track',)
    ordering = ('uploaded_at',)


admin.site.register(models.Video, MusicAdmin)
admin.site.register(models.Audio, MusicAdmin)
