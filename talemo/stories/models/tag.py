"""
Tag model for the stories app.
"""
from django.db import models
import uuid

class Tag(models.Model):
    """
    Model for storing tags for stories.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.CharField(
        max_length=50,
        choices=[
            ('theme', 'Theme'),
            ('character', 'Character'),
            ('mood', 'Mood'),
            ('setting', 'Setting'),
            ('age_range', 'Age Range'),
            ('other', 'Other'),
        ],
        default='theme'
    )

    class Meta:
        app_label = 'stories'
        unique_together = ('tenant', 'slug')

    def __str__(self):
        return self.name
