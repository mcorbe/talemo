"""
Story model for the stories app.
"""
from django.db import models
import uuid


class Story(models.Model):
    """
    Model for storing stories.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="The title of the story")
    description = models.TextField(help_text="A brief description of the story")
    age_group = models.CharField(max_length=255, help_text="The age group for the story")
    topic = models.CharField(max_length=255, help_text="The main topic of the story")
    hero = models.CharField(max_length=255, help_text="The main character of the story")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
