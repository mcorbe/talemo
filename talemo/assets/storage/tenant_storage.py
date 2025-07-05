"""
Custom storage class for tenant-specific asset storage.
"""
from django.conf import settings
from django.utils.module_loading import import_string
from storages.backends.s3boto3 import S3Boto3Storage
from django_tenants.utils import get_tenant_model, get_current_schema_name


class TenantS3Boto3Storage(S3Boto3Storage):
    """
    Storage class that prefixes file paths with the tenant schema name.
    This ensures tenant isolation for all stored assets.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tenant_prefix = None

    def get_tenant_prefix(self):
        """
        Get the tenant prefix for the current request.
        """
        if self.tenant_prefix is None:
            try:
                # Try to get the current schema name from the thread local
                schema_name = get_current_schema_name()
                if schema_name:
                    self.tenant_prefix = schema_name
                else:
                    # Fallback to public schema if no tenant is set
                    self.tenant_prefix = 'public'
            except Exception:
                # If there's any error, use a safe default
                self.tenant_prefix = 'public'
        return self.tenant_prefix

    def _normalize_name(self, name):
        """
        Normalize the file path by adding the tenant prefix.
        """
        name = super()._normalize_name(name)
        prefix = self.get_tenant_prefix()
        
        # If the name already starts with the prefix, don't add it again
        if name.startswith(f"{prefix}/"):
            return name
        
        return f"{prefix}/{name}"