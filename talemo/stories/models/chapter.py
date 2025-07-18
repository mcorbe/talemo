"""
Chapter model for the stories app.
"""
from django.db import models
import uuid
from django.conf import settings

class Chapter(models.Model):
    """
    Model for storing story chapters.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="The chapter text")
    place = models.CharField(max_length=255, help_text="The place where the chapter takes place")
    tool = models.CharField(max_length=255, help_text="The tool used in the chapter")
    order = models.PositiveIntegerField(default=1, help_text="The order of the chapter in the story")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.story.title} - #{self.order}: {self.title}"