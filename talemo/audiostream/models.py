from django.db import models

class AudioSession(models.Model):
    session_id       = models.CharField(max_length=32, primary_key=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    status           = models.CharField(max_length=12, default="pending") # pending|running|ready|error
    playlist_rel_url = models.CharField(max_length=200, blank=True)
    error_message    = models.TextField(blank=True)