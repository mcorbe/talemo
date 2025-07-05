"""
Storage module for asset management.
"""
from .storage import CustomS3Boto3Storage

# Create a default instance of the storage
default_storage = CustomS3Boto3Storage()
