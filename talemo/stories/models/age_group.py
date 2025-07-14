"""
AgeGroup model for the stories app.
"""
from django.db import models
import uuid

class AgeGroup(models.Model):
    """
    Model for storing age groups for stories.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age_range = models.CharField(
        max_length=20,
        help_text="Age range (e.g., '0 - 2', '3 - 5')"
    )
    common_label = models.CharField(
        max_length=50,
        help_text="Common label for this age group (e.g., 'Board-book / Infant', 'Picture-book (Pre-K)')"
    )
    typical_traits = models.TextField(
        help_text="Typical story and format traits for this age group"
    )
    classic_examples = models.TextField(
        help_text="Classic examples of stories for this age group"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'stories'
        verbose_name = 'Age Group'
        verbose_name_plural = 'Age Groups'
        ordering = ['age_range']

    def __str__(self):
        return f"{self.common_label} ({self.age_range})"