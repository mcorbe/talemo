"""
Tenant policy models for the core app.
"""
from django.db import models
import uuid


class TenantPolicy(models.Model):
    """
    Tenant policy model for the core app.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='policies')
    key = models.CharField(max_length=100)
    value = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_tenant_policy'
        unique_together = ('tenant', 'key')

    def __str__(self):
        return f"{self.tenant.name} - {self.key}"