"""
Story model for the stories app.
"""
from django.db import models
import uuid
from django.conf import settings

class Story(models.Model):
    """
    Model for storing story_list.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(help_text="The story text")
    language = models.CharField(
        max_length=10,
        default='fr-FR',
        help_text="Language code (e.g., fr-FR, en-US)"
    )
    age_range = models.CharField(
        max_length=10,
        choices=[
            ('0-3', '0-3 years'),
            ('4-6', '4-6 years'),
            ('7-9', '7-9 years'),
            ('10-12', '10-12 years'),
            ('13+', '13+ years'),
        ],
        default='4-6'
    )
    duration = models.IntegerField(
        default=0,
        help_text="Duration in seconds"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_stories'
    )
    visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('tenant_only', 'Tenant Only'),
            ('private', 'Private'),
        ],
        default='tenant_only'
    )
    is_published = models.BooleanField(default=False)
    is_ai_generated = models.BooleanField(
        default=True,
        help_text="For AI Act compliance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'story_list'
        verbose_name_plural = 'story_list'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
