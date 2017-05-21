from django.contrib import admin
from . import models


class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'year', 'disc', 'track',)
    ordering = ('uploaded_at',)


class CompilationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created',)
    ordering = ('created',)


admin.site.register(models.Video, MusicAdmin)
admin.site.register(models.Audio, MusicAdmin)
admin.site.register(models.AudioCompilation, CompilationAdmin)
admin.site.register(models.VideoCompilation, CompilationAdmin)
