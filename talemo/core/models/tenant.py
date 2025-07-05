"""
Tenant models for multi-tenant functionality.
"""
from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant model for multi-tenant functionality.
    """
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

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
