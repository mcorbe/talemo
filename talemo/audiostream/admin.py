from django.contrib import admin
from django.utils.html import format_html
from .models import AudioSession

class AudioSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'created_at', 'status_colored', 'playlist_rel_url')
    list_filter = ('status', 'created_at')
    search_fields = ('session_id', 'playlist_rel_url')
    readonly_fields = ('created_at',)

    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'running': 'blue',
            'ready': 'green',
            'error': 'red',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.status)

    status_colored.short_description = 'Status'

admin.site.register(AudioSession, AudioSessionAdmin)
