"""
Story model for the stories app.
"""
from django.db import models
import uuid
from django.conf import settings
from .age_group import AgeGroup

class Story(models.Model):
    """
    Model for storing stories.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.CharField(max_length=255, help_text="The main topic of the story")
    hero = models.CharField(max_length=255, help_text="The main character of the story")
    # content field is now moved to Chapter model
    language = models.CharField(
        max_length=10,
        default='fr-FR',
        help_text="Language code (e.g., fr-FR, en-US)"
    )
    age_group = models.ForeignKey(
        AgeGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stories',
        help_text="The target age group for this story"
    )
    total_duration = models.IntegerField(
        default=0,
        help_text="Total duration of all chapters in seconds"
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
        app_label = 'stories'
        verbose_name_plural = 'stories'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
