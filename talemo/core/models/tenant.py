"""
Tenant models for multi-tenant functionality.
"""
from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    """
    Tenant model for multi-tenant functionality.
    """
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_tenant'

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Domain model for multi-tenant functionality.
    """
    domain = models.CharField(max_length=253, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_domain'

    def __str__(self):
        return self.domain