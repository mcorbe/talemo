"""
Tenant models for shared schema functionality.
"""
from django.db import models
import uuid


class Tenant(models.Model):
    """
    Tenant model for shared schema functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=[
            ('family', 'Family'),
            ('institution', 'Institution'),
        ],
        default='family'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_tenant'

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Domain model for shared schema functionality.
    """
    domain = models.CharField(max_length=253, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_domain'

    def __str__(self):
        return self.domain
