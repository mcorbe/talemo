"""
Tenant models for multi-tenant functionality.
"""
from django.db import models
import uuid
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant model for multi-tenant functionality.
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

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    class Meta:
        db_table = 'core_tenant'

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for multi-tenant functionality.
    """
    is_primary = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_domain'

    def __str__(self):
        return self.domain
