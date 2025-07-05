"""
Asset model for the assets app.
"""
from django.db import models
import uuid

class Asset(models.Model):
    """
    Model for storing assets (images, audio files, etc.).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='assets')
    type = models.CharField(
        max_length=20,
        choices=[
            ('image', 'Image'),
            ('audio', 'Audio'),
            ('user_audio', 'User Audio'),
        ],
        default='image'
    )
    file_path = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=100)
    source_task = models.ForeignKey(
        'agents.AgentTask',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_assets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = 'assets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.id}"
