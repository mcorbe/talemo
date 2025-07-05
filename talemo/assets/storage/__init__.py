"""
Storage module for asset management.
"""
from .tenant_storage import TenantS3Boto3Storage

# Create a default instance of the tenant storage
default_storage = TenantS3Boto3Storage()
