"""
User profile models.
"""
from django.db import models
import uuid
from django_tenants.models import TenantMixin


class Profile(models.Model):
    """
    User profile model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=100)
    permissions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_profile'
        unique_together = ('tenant', 'name')

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
