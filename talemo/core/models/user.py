"""
User models for the core app.
"""
from django.db import models
import uuid


class User(models.Model):
    """
    User model for the core app.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='users')
    profile = models.ForeignKey('core.Profile', on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'core_user'

    def __str__(self):
        return f"{self.name} ({self.email})"